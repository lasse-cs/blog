from dataclasses import dataclass, field

from django.contrib.syndication.views import Feed
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.feedgenerator import Atom1Feed
from django.views.decorators.vary import vary_on_headers

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, ItemBase

from wagtail.admin.panels import FieldPanel
from wagtail.blocks import ListBlock, StreamBlock, StructBlock
from wagtail.contrib.routable_page.models import path
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.images import get_image_model

from core.blocks import HeadingBlock, SocialLinkBlock, HeadingLevelChoices
from core.utilities import paginate


Image = get_image_model()


@dataclass
class TableOfContentsItem:
    level: str
    heading: str
    children: list["TableOfContentsItem"] = field(default_factory=list)


class BaseRSSFeed(Feed):
    description_template = "patterns/feeds/description.html"

    def get_object(self, request, page):
        return page

    def title(self, obj):
        return obj.feed_title()

    def description(self, obj):
        return obj.feed_description()

    def link(self, obj):
        return obj.url

    def items(self, obj):
        number = getattr(obj, "per_page", 30)
        return obj.get_feed_items()[:number]

    def item_title(self, item):
        return item.feed_title()

    def item_link(self, item):
        return item.url

    def item_pubdate(self, item):
        return item.first_published_at


class BaseAtomFeed(BaseRSSFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj):
        return self.description(obj)


class FeedMixin:
    rss_feed_instance = BaseRSSFeed()
    atom_feed_instance = BaseAtomFeed()
    per_page = 10

    def feed_title(self):
        return self.seo_title or self.title

    def feed_description(self):
        return self.search_description or f"Feed for {self.feed_title()}"

    @path("rss/", name="rss")
    def rss_feed(self, request):
        return self.rss_feed_instance(request, self)

    @path("atom/", name="atom")
    def atom_feed(self, request):
        return self.atom_feed_instance(request, self)

    def get_feed_items(self):
        return (
            self.get_children()
            .type(FeedItemMixin)
            .live()
            .public()
            .specific()
            .order_by("-first_published_at")
        )

    def get_paginated_feed_items(self, page_number):
        items = self.get_feed_items()
        return paginate(page_number, items, self.per_page)


class FeedItemMixin(models.Model):
    """
    Mixin to specify that a model can be included in a Feed.
    """

    intro = RichTextField(
        help_text="Intro text for the page, used also in summaries.",
        default="Intro content.",
    )

    panels = [
        FieldPanel("intro"),
    ]

    search_fields = [
        index.SearchField("intro"),
    ]

    def feed_title(self):
        return self.seo_title or self.title

    def get_summary_template(self):
        if hasattr(self, "summary_template"):
            return self.summary_template
        raise NotImplementedError("You must define summary_template on the model.")

    class Meta:
        abstract = True


class TableOfContentsMixin:
    toc_source_fields = []
    toc_max_level = HeadingLevelChoices.H3

    @property
    def table_of_contents(self):
        level_order = {
            HeadingLevelChoices.H2: 2,
            HeadingLevelChoices.H3: 3,
            HeadingLevelChoices.H4: 4,
        }
        max_level = level_order[self.toc_max_level]

        toc = []
        stack = []

        for toc_source_field in self.toc_source_fields:
            stream_value = getattr(self, toc_source_field, None)
            for level, heading in self._walk_headings(None, stream_value):
                order = level_order[level]
                if order > max_level:
                    continue

                node = TableOfContentsItem(level=level, heading=heading)
                while stack and stack[-1][0] >= order:
                    stack.pop()
                if stack:
                    stack[-1][1].children.append(node)
                else:
                    toc.append(node)
                stack.append((order, node))
        return toc

    def _walk_headings(self, block, value):
        if value is None:
            return

        # We're at the top StreamValue
        if block is None:
            for child in value:
                yield from self._walk_headings(child.block, child.value)

        # We're at a heading block
        elif isinstance(block, HeadingBlock):
            yield (value["level"], value["heading"])

        # We're at a StreamBlock
        elif isinstance(block, StreamBlock):
            for child in value:
                yield from self._walk_headings(child.block, child.value)

        # We're at a StructBlock
        elif isinstance(block, StructBlock):
            for name, child_def in block.child_blocks.items():
                yield from self._walk_headings(child_def, value.get(name))

        # We're at a ListBlock
        elif isinstance(block, ListBlock):
            for item in value:
                item_block = block.child_block
                yield from self._walk_headings(item_block, item)


@register_setting
class SiteFooter(BaseSiteSetting):
    content = RichTextField(
        "Footer Content", max_length=255, features=["italic", "link", "bold"]
    )


@register_setting
class SocialMediaLinks(BaseSiteSetting):
    links = StreamField(
        [
            ("link", SocialLinkBlock()),
        ],
        help_text="Social Media Links",
    )


@register_setting
class SEOSettings(BaseSiteSetting):
    og_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The default og_image for this Site",
    )


class PageTag(TagBase):
    def get_absolute_url(self):
        return reverse("tagged_pages", args=(self.slug,))


class TaggedPage(ItemBase):
    tag = models.ForeignKey(
        PageTag,
        related_name="tagged_pages",
        on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        to="core.TaggablePage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )

    def __str__(self):
        return f"{self.tag} - {self.content_object}"


class TaggablePage(Page):
    """
    Base for a page that supports tags.
    Use a separate "pool" of tags from the default taggit Tag model.

    Use a separate concrete (non-creatable) base class to allow multiple
    page models to share the pool of tags.
    """

    tags = ClusterTaggableManager(through="core.TaggedPage", blank=True)

    # is_creatable is not inherited by subclasses
    is_creatable = False

    promote_panels = Page.promote_panels + [
        FieldPanel("tags"),
    ]

    def get_tag_summary_template(self):
        if hasattr(self, "tag_summary_template"):
            return self.tag_summary_template
        if hasattr(self, "summary_template"):
            return self.summary_template
        raise NotImplementedError(
            "You must define a tag_summary_template or summary_template."
        )


class MarkdownPageMixin:
    @property
    def preview_modes(self):
        return [*super().preview_modes, ("markdown", "Markdown")]

    def is_markdown_request(self, request):
        if request.GET.get("format") == "md":
            return True
        content_type = request.get_preferred_type(["text/html", "text/markdown"])
        return content_type == "text/markdown"

    @method_decorator(vary_on_headers("Accept"))
    def serve(self, request, *args, **kwargs):
        request.is_markdown = self.is_markdown_request(request)
        if request.is_markdown:
            response = self.serve_markdown(request, *args, **kwargs)
        else:
            response = super().serve(request, *args, **kwargs)
        return response

    def serve_preview(self, request, mode_name):
        if mode_name == "markdown":
            request.is_markdown = True
            request.is_preview = True
            return self.serve_markdown(request)
        return super().serve_preview(request, mode_name)

    def get_markdown_template(self, request, *args, **kwargs):
        try:
            return self.markdown_template
        except AttributeError as e:
            raise ImproperlyConfigured("No markdown template provided") from e

    def get_markdown_context(self, request, *args, **kwargs):
        return self.get_context(request, *args, **kwargs)

    def serve_markdown(self, request, *args, **kwargs):
        request.is_preview = getattr(request, "is_preview", False)
        request.is_markdown = True
        response = TemplateResponse(
            request,
            self.get_markdown_template(request, *args, **kwargs),
            self.get_markdown_context(request, *args, **kwargs),
        )
        response.headers["Content-Type"] = "text/markdown; charset=utf-8"
        return response


class MarkdownRoutablePageMixin:
    @path("")
    def index(self, request, *args, **kwargs):
        request.is_preview = getattr(request, "is_preview", False)
        return self.render(request, *args, **kwargs)

    def serve(self, request, view=None, args=None, kwargs=None):
        request.is_markdown = self.is_markdown_request(request)
        return super().serve(request, view, args, kwargs)

    def render_markdown(
        self, request, *args, template=None, context_overrides=None, **kwargs
    ):
        if template is None:
            template = self.get_markdown_template(request, *args, **kwargs)
        context = self.get_markdown_context(request, *args, **kwargs)
        context.update(context_overrides or {})
        response = TemplateResponse(request, template, context)
        response.headers["Content-Type"] = "text/markdown; charset=utf-8"
        return response

    def serve_preview(self, request, mode_name):
        if mode_name == "markdown":
            request.is_markdown = True
            request.is_preview = True
        return super().serve_preview(request, mode_name)

    @method_decorator(vary_on_headers("Accept"))
    def render(self, request, *args, template=None, context_overrides=None, **kwargs):
        if getattr(request, "is_markdown", False):
            return self.render_markdown(
                request,
                *args,
                template=template,
                context_overrides=context_overrides,
                **kwargs,
            )
        return super().render(
            request,
            *args,
            template=template,
            context_overrides=context_overrides,
            **kwargs,
        )

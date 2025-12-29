from django.contrib.syndication.views import Feed
from django.db import models
from django.utils.feedgenerator import Atom1Feed

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index

from core.blocks import SocialLinkBlock
from core.utilities import paginate


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
        return self.descripion(obj)


class FeedMixin(RoutablePageMixin):
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

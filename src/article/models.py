from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from core.models import FeedItemMixin, FeedMixin


class ArticleIndexPage(FeedMixin, Page):
    subpage_types = ["article.ArticlePage"]

    template = "patterns/pages/article/article_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["articles"] = self.get_feed_items()
        return context


class ArticlePage(FeedItemMixin, Page):
    intro = RichTextField(
        help_text="Intro text for the article page.",
        default="Article intro content.",
    )
    body = StreamField(
        [
            (
                "text",
                RichTextBlock(
                    template="patterns/components/streamfield/blocks/text.html"
                ),
            ),
        ],
        help_text="Main body content for the article page.",
    )

    content_panels = Page.content_panels + FeedItemMixin.panels + [
        FieldPanel("body"),
    ]

    search_fields = (
        Page.search_fields
        + FeedItemMixin.search_fields
        + [
            index.SearchField("body"),
        ]
    )

    parent_page_types = ["article.ArticleIndexPage"]
    subpage_types = []

    summary_template = "patterns/components/article/article_summary.html"
    template = "patterns/pages/article/article_page.html"

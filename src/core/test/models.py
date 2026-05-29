from django.http import JsonResponse

from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import StreamField
from wagtail.models import Page

from core.blocks import HeadingLevelChoices
from core.models import (
    TaggablePage,
    TableOfContentsMixin,
    MarkdownPageMixin,
    MarkdownRoutablePageMixin,
)

from core.test.blocks import TableOfContentsBlock


class PageWithTags(TaggablePage):
    summary_template = "test/summary.html"


class AnotherPageWithTags(TaggablePage):
    summary_template = "test/summary.html"


class PageWithTableOfContents(TableOfContentsMixin, Page):
    toc_source_fields = ["body"]
    toc_max_level = HeadingLevelChoices.H4

    body = StreamField(TableOfContentsBlock)


class PageWithTableOfContentsH3(TableOfContentsMixin, Page):
    toc_source_fields = ["body"]

    body = StreamField(TableOfContentsBlock)


class MarkdownViewablePage(MarkdownPageMixin, Page):
    template = "test/markdown_page.html"
    markdown_template = "test/markdown_page.md"


class NoTemplateMarkdownPage(MarkdownPageMixin, Page):
    pass


class MarkdownRoutablePage(
    MarkdownRoutablePageMixin, RoutablePageMixin, MarkdownPageMixin, Page
):
    template = "test/markdown_page.html"
    markdown_template = "test/markdown_page.md"

    @path("not-markdown", name="not-markdown")
    def not_markdown(self, request):
        return JsonResponse(data={"key": "value"})


class NoTemplateMarkdownRoutablePage(
    MarkdownRoutablePageMixin, RoutablePageMixin, MarkdownPageMixin, Page
):
    pass

from wagtail.fields import StreamField
from wagtail.models import Page

from core.blocks import HeadingLevelChoices
from core.models import TaggablePage, TableOfContentsMixin

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

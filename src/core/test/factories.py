import factory
from wagtail_factories import (
    ListBlockFactory,
    PageFactory,
    StreamBlockFactory,
    StreamFieldFactory,
    StructBlockFactory,
)

from core.factories import HeadingBlockFactory, TaggablePageFactory
from core.test.blocks import (
    HeadingStreamBlock,
    HeadingStructBlock,
    TableOfContentsBlock,
)
from core.test.models import (
    AnotherPageWithTags,
    MarkdownRoutablePage,
    MarkdownViewablePage,
    NoTemplateMarkdownPage,
    NoTemplateMarkdownRoutablePage,
    PageWithTableOfContents,
    PageWithTableOfContentsH3,
    PageWithTags,
)


class PageWithTagsFactory(TaggablePageFactory):
    class Meta:
        model = PageWithTags


class AnotherPageWithTagsFactory(TaggablePageFactory):
    class Meta:
        model = AnotherPageWithTags


class HeadingStructBlockFactory(StructBlockFactory):
    heading = factory.SubFactory(HeadingBlockFactory)

    class Meta:
        model = HeadingStructBlock


class HeadingStreamBlockFactory(StreamBlockFactory):
    heading = factory.SubFactory(HeadingBlockFactory)

    class Meta:
        model = HeadingStreamBlock


class TableOfContentBlockFactory(StreamBlockFactory):
    heading = factory.SubFactory(HeadingBlockFactory)
    heading_list = ListBlockFactory(HeadingBlockFactory)
    heading_struct = factory.SubFactory(HeadingStructBlockFactory)
    heading_stream = StreamFieldFactory(HeadingStreamBlockFactory)

    class Meta:
        model = TableOfContentsBlock


class PageWithTableOfContentsFactory(PageFactory):
    body = StreamFieldFactory(TableOfContentBlockFactory)

    class Meta:
        model = PageWithTableOfContents


class PageWithTableOfContentsH3Factory(PageFactory):
    body = StreamFieldFactory(TableOfContentBlockFactory)

    class Meta:
        model = PageWithTableOfContentsH3


class MarkdownViewablePageFactory(PageFactory):
    class Meta:
        model = MarkdownViewablePage


class NoTemplateMarkdownPageFactory(PageFactory):
    class Meta:
        model = NoTemplateMarkdownPage


class MarkdownRoutablePageFactory(PageFactory):
    class Meta:
        model = MarkdownRoutablePage


class NoTemplateMarkdownRoutablePageFactory(PageFactory):
    class Meta:
        model = NoTemplateMarkdownRoutablePage

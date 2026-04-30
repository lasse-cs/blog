import factory

from wagtail_factories import (
    PageFactory,
    StreamBlockFactory,
    StreamFieldFactory,
    StructBlockFactory,
    ListBlockFactory,
)

from core.factories import TaggablePageFactory, HeadingBlockFactory

from core.test.blocks import (
    TableOfContentsBlock,
    HeadingStreamBlock,
    HeadingStructBlock,
)
from core.test.models import (
    AnotherPageWithTags,
    PageWithTags,
    PageWithTableOfContents,
    PageWithTableOfContentsH3,
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

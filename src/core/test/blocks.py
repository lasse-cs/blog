from wagtail.blocks import StreamBlock, ListBlock, StructBlock

from core.blocks import HeadingBlock


class HeadingStructBlock(StructBlock):
    heading = HeadingBlock()


class HeadingStreamBlock(StreamBlock):
    heading = HeadingBlock()


class TableOfContentsBlock(StreamBlock):
    heading = HeadingBlock()
    heading_list = ListBlock(HeadingBlock)
    heading_struct = HeadingStructBlock()
    heading_stream = HeadingStreamBlock()

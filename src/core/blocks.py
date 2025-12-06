from wagtail.blocks import CharBlock, RichTextBlock, StreamBlock, StructBlock


class TitledTextBlock(StructBlock):
    title = CharBlock(
        required=True,
        help_text="The title of this block.",
        max_length=60,
    )
    text = RichTextBlock(
        required=True,
        help_text="The text of this block.",
    )

    class Meta:
        template = "patterns/components/sidebar/blocks/titled_text_block.html"


class SidebarBlock(StreamBlock):
    text = TitledTextBlock()

    class Meta:
        template = "patterns/components/sidebar/sidebar.html"

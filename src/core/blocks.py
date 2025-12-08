from django.db import models

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)


class SocialMediaChoices(models.TextChoices):
    GITHUB = "github", "GitHub"
    BLUESKY = "bluesky", "BlueSky"
    FEED = "feed", "Feed"


class SocialLinkBlock(StructBlock):
    display = CharBlock(
        required=True,
        help_text="The display text of this social media link",
        max_length=60,
    )
    url = URLBlock(required=True, help_text="The URL of this social media link")
    type = ChoiceBlock(
        choices=SocialMediaChoices.choices,
        default=SocialMediaChoices.GITHUB,
        help_text="The type of social media link",
        required=True,
    )


class BaseSidebarItemBlock(StructBlock):
    title = CharBlock(
        required=True,
        help_text="The title of this block.",
        max_length=60,
    )


class TitledTextBlock(BaseSidebarItemBlock):
    text = RichTextBlock(
        required=True,
        help_text="The text of this block.",
    )

    class Meta:
        template = "patterns/components/sidebar/blocks/titled_text_block.html"
        icon = "doc-full-inverse"


class SocialBlock(BaseSidebarItemBlock):
    class Meta:
        template = "patterns/components/sidebar/blocks/social_block.html"
        icon = "link-external"


class SidebarBlock(StreamBlock):
    text = TitledTextBlock()
    social = SocialBlock()

    class Meta:
        template = "patterns/components/sidebar/sidebar.html"
        block_counts = {
            "social": {"max_num": 1},
        }

from django.db import models

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)

from wagtailcodeblock.blocks import CodeBlock


class ContentBlock(StreamBlock):
    text = RichTextBlock(template="patterns/components/streamfield/blocks/text.html")
    code = CodeBlock(template="patterns/components/streamfield/blocks/code.html")


class SocialMediaChoices(models.TextChoices):
    GITHUB = "github", "GitHub"
    BLUESKY = "bluesky", "BlueSky"
    LINKEDIN = "linkedin", "LinkedIn"
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


class ActivityBlock(BaseSidebarItemBlock):
    class Meta:
        template = "patterns/components/sidebar/blocks/activity_block.html"


class SidebarBlock(StreamBlock):
    text = TitledTextBlock()
    social = SocialBlock()
    activity = ActivityBlock()

    class Meta:
        template = "patterns/components/sidebar/sidebar.html"
        block_counts = {
            "social": {"max_num": 1},
            "activity": {"max_num": 1},
        }

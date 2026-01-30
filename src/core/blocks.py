from django.db import models

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)

from wagtailcodeblock.blocks import CodeBlock


class HeadingLevelChoices(models.TextChoices):
    H2 = "h2", "h2"
    H3 = "h3", "h3"
    H4 = "h4", "h4"


class HeadingBlock(StructBlock):
    level = ChoiceBlock(
        choices=HeadingLevelChoices.choices,
        default=HeadingLevelChoices.H2,
        help_text="The level of this heading",
        required=True,
    )
    heading = TextBlock(
        max_length=127,
        help_text="The text for this heading",
        required=True,
    )

    class Meta:
        icon = "title"
        template = "patterns/components/streamfield/blocks/heading.html"


class ContentBlock(StreamBlock):
    text = RichTextBlock(template="patterns/components/streamfield/blocks/text.html")
    code = CodeBlock(template="patterns/components/streamfield/blocks/code.html")
    heading = HeadingBlock()


class SocialMediaChoices(models.TextChoices):
    GITHUB = "github", "GitHub"
    BLUESKY = "bluesky", "BlueSky"
    LINKEDIN = "linkedin", "LinkedIn"
    FEED = "feed", "Feed"
    TWITTER = "twitter", "Twitter"


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


class TagBlock(BaseSidebarItemBlock):
    class Meta:
        template = "patterns/components/sidebar/blocks/tag_block.html"

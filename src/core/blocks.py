from django.db import models
from django.utils.encoding import force_bytes

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    StructValue,
    TextBlock,
    URLBlock,
)
from wagtail.coreutils import safe_md5


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
        preview_value = {
            "level": HeadingLevelChoices.H2,
            "heading": "This is the Heading",
        }


class CodeLanguageChoices(models.TextChoices):
    BASH = "bash", "Bash/Shell"
    CSS = "css", "CSS"
    DIFF = "diff", "diff"
    HTML = "html", "HTML"
    JAVASCRIPT = "javascript", "JavaScript"
    JSON = "json", "JSON"
    PYTHON = "python", "Python"
    SCSS = "scss", "SCSS"
    YAML = "yaml", "YAML"


CODE_BLOCK_CACHE_TIMEOUT = 60 * 60 * 24 * 7


class CodeBlockValue(StructValue):
    cache_timeout = CODE_BLOCK_CACHE_TIMEOUT

    def get_cache_key_components(self):
        return ["code-block", self.get("language", ""), self.get("code", ""), "v1"]

    @property
    def cache_key(self):
        hasher = safe_md5()

        for component in self.get_cache_key_components():
            hasher.update(force_bytes(component))

        return hasher.hexdigest()


class CodeBlock(StructBlock):
    language = ChoiceBlock(
        choices=CodeLanguageChoices.choices,
        help_text="Coding language",
        label="Language",
    )
    code = TextBlock(label="Code")

    class Meta:
        icon = "code"
        template = "patterns/components/streamfield/blocks/code.html"
        value_class = CodeBlockValue


class ContentBlock(StreamBlock):
    text = RichTextBlock(
        template="patterns/components/streamfield/blocks/text.html",
        preview_value="<b>Rich text</b> content",
    )
    code = CodeBlock(
        template="patterns/components/streamfield/blocks/code.html",
        preview_value={
            "language": "python",
            "code": 'if __name__ == "__main__":\n    print("Hello World!")',
        },
    )
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
        preview_value = {"title": "Title", "text": "<b>Rich text</b> content."}


class SocialBlock(BaseSidebarItemBlock):
    class Meta:
        template = "patterns/components/sidebar/blocks/social_block.html"
        icon = "link-external"
        preview_value = {"title": "Social"}


class TagBlock(BaseSidebarItemBlock):
    class Meta:
        template = "patterns/components/sidebar/blocks/tag_block.html"
        preview_value = {"title": "Tags"}

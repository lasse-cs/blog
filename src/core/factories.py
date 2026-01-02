import factory
from factory.django import DjangoModelFactory

from wagtail.blocks import RichTextBlock
from wagtail.rich_text import RichText

from wagtailcodeblock.blocks import CodeBlock

from wagtail_factories import (
    PageFactory,
    SiteFactory,
    StreamBlockFactory,
    StreamFieldFactory,
    StructBlockFactory,
)
from wagtail_factories.blocks import BlockFactory

from core.blocks import (
    ActivityBlock,
    BaseSidebarItemBlock,
    ContentBlock,
    SidebarBlock,
    SocialBlock,
    SocialLinkBlock,
    SocialMediaChoices,
    TagBlock,
    TitledTextBlock,
)
from core.models import AnalyticsSettings, SiteFooter, SocialMediaLinks, TaggablePage


class RichTextBlockFactory(BlockFactory):
    class Meta:
        model = RichTextBlock


class SocialLinkBlockFactory(StructBlockFactory):
    display = factory.Faker("text", max_nb_chars=60)
    url = factory.Faker("uri")
    type = factory.Faker("random_element", elements=SocialMediaChoices.values)

    class Meta:
        model = SocialLinkBlock


class BaseSidebarItemBlockFactory(StructBlockFactory):
    title = factory.Faker("text", max_nb_chars=60)

    class Meta:
        model = BaseSidebarItemBlock


class TitledTextBlockFactory(BaseSidebarItemBlockFactory):
    text = factory.SubFactory(RichTextBlockFactory)

    class Meta:
        model = TitledTextBlock


class SocialBlockFactory(BaseSidebarItemBlockFactory):
    class Meta:
        model = SocialBlock


class ActivityBlockFactory(BaseSidebarItemBlockFactory):
    class Meta:
        model = ActivityBlock


class TagBlockFactory(BaseSidebarItemBlockFactory):
    class Meta:
        model = TagBlock


class SidebarBlockFactory(StreamBlockFactory):
    text = factory.SubFactory(TitledTextBlockFactory)
    social = factory.SubFactory(SocialBlockFactory)
    activity = factory.SubFactory(ActivityBlockFactory)
    tag = factory.SubFactory(TagBlockFactory)

    class Meta:
        model = SidebarBlock


class CodeBlockFactory(StructBlockFactory):
    language = "python"
    code = "print('Hello World!')"

    class Meta:
        model = CodeBlock


class ContentBlockFactory(StreamBlockFactory):
    text = factory.SubFactory(RichTextBlockFactory)
    code = factory.SubFactory(CodeBlockFactory)

    class Meta:
        model = ContentBlock


class SocialMediaLinksFactory(DjangoModelFactory):
    site = factory.SubFactory(SiteFactory)
    links = StreamFieldFactory({"link": SocialLinkBlockFactory()})

    class Meta:
        model = SocialMediaLinks


class SiteFooterFactory(DjangoModelFactory):
    site = factory.SubFactory(SiteFactory)
    content = RichText("<b>This is the Site Footer</b>")

    class Meta:
        model = SiteFooter


class AnalyticsSettingsFactory(DjangoModelFactory):
    site = factory.SubFactory(SiteFactory)
    umami_id = factory.Faker("uuid4")

    class Meta:
        model = AnalyticsSettings


class TaggablePageFactory(PageFactory):
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.tags.add(*extracted)

    class Meta:
        model = TaggablePage

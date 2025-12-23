import factory
from factory.django import DjangoModelFactory

from wagtail.blocks import RichTextBlock
from wagtail.rich_text import RichText

from wagtail_factories import (
    SiteFactory,
    StreamBlockFactory,
    StreamFieldFactory,
    StructBlockFactory,
)
from wagtail_factories.blocks import BlockFactory

from core.blocks import (
    BaseSidebarItemBlock,
    SidebarBlock,
    SocialBlock,
    SocialLinkBlock,
    SocialMediaChoices,
    TitledTextBlock,
)
from core.models import SiteFooter, SocialMediaLinks


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


class SidebarBlockFactory(StreamBlockFactory):
    text = factory.SubFactory(TitledTextBlockFactory)
    social = factory.SubFactory(SocialBlockFactory)

    class Meta:
        model = SidebarBlock


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

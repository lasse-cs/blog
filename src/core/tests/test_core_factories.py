import pytest
from core.factories import (
    ContentBlockFactory,
    SiteFooterFactory,
    SocialMediaLinksFactory,
)

from wagtail.rich_text import RichText


@pytest.mark.django_db
def test_social_media_links_factory():
    social_media_links = SocialMediaLinksFactory(**{"links__0": "link"})
    assert len(social_media_links.links) == 1


@pytest.mark.django_db
def test_site_footer_factory():
    site_footer = SiteFooterFactory()
    assert site_footer.content == RichText("<b>This is the Site Footer</b>")


def test_content_block_factory():
    content_block = ContentBlockFactory(**{"0": "text"})
    assert len(content_block) == 1

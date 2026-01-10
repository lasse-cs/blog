import pytest
from core.factories import (
    ContentBlockFactory,
    SiteFooterFactory,
    SocialMediaLinksFactory,
    TaggablePageFactory,
)

from wagtail.rich_text import RichText


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("site"),
]


def test_social_media_links_factory():
    social_media_links = SocialMediaLinksFactory(**{"links__0": "link"})
    assert len(social_media_links.links) == 1


def test_site_footer_factory():
    site_footer = SiteFooterFactory()
    assert site_footer.content == RichText("<b>This is the Site Footer</b>")


def test_content_block_factory():
    content_block = ContentBlockFactory(**{"0": "text", "1": "code"})
    assert len(content_block) == 2


def test_taggable_page_factory():
    taggable_page = TaggablePageFactory(tags=["red", "green", "blue"])
    assert set(taggable_page.tags.all().values_list("name", flat=True)) == {
        "red",
        "green",
        "blue",
    }

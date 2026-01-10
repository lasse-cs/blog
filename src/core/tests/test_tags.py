import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains

from django.urls import reverse

from core.models import PageTag
from core.test.factories import PageWithTagsFactory


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("site"),
]


def test_page_tag_absolute_url():
    tag = PageTag(name="tag_name", slug="tag_slug")
    assert tag.get_absolute_url() == reverse("tagged_pages", args=(tag.slug,))


def test_not_found_for_non_tag(client):
    response = client.get(reverse("tagged_pages", args=("not-a-real-tag",)))
    assert response.status_code == 404


def test_routable_for_existing_tag(client):
    tag = PageTag.objects.create(name="tag", slug="tag")
    response = client.get(tag.get_absolute_url())
    assert response.status_code == 200


def test_uses_correct_template(client):
    tag = PageTag.objects.create(name="tag", slug="tag")
    response = client.get(tag.get_absolute_url())
    assertTemplateUsed(response, "patterns/pages/core/tagged_pages.html")


def test_shows_all_live_tagged_pages(client, root_page):
    live_with_tags = PageWithTagsFactory(
        tags=["tag1", "tag2"], parent=root_page, title="LiveTags"
    )
    live_without_tags = PageWithTagsFactory(parent=root_page, title="LiveNoTags")
    dead_with_tags = PageWithTagsFactory(
        parent=root_page,
        tags=["tag1"],
        live=False,
        title="DeadTags",
    )
    response = client.get(reverse("tagged_pages", args=("tag1",)))
    assertContains(response, live_with_tags.title)
    assertNotContains(response, live_without_tags.title)
    assertNotContains(response, dead_with_tags.title)

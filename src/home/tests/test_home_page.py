import pytest
from pytest_django.asserts import assertTemplateUsed

from wagtail.models import Page

from home.factories import HomePageFactory
from home.models import HomePage


def test_home_page_can_only_be_created_under_root():
    assert set(HomePage.allowed_parent_page_models()) == {Page}


@pytest.mark.django_db
def test_home_page_is_routable(client, root_page):
    home_page = HomePageFactory(parent=root_page)
    response = client.get(home_page.url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_page_template(client, root_page):
    home_page = HomePageFactory(parent=root_page)
    response = client.get(home_page.url)
    assertTemplateUsed(response, "patterns/pages/home/home_page.html")


@pytest.mark.django_db
def test_home_page_renders_sidebar(client, root_page):
    home_page = HomePageFactory(
        parent=root_page, sidebar__0="text", sidebar__1="social"
    )
    response = client.get(home_page.url)
    assertTemplateUsed(response, "patterns/components/sidebar/sidebar.html")
    assertTemplateUsed(
        response, "patterns/components/sidebar/blocks/social_block.html", count=1
    )
    assertTemplateUsed(
        response, "patterns/components/sidebar/blocks/titled_text_block.html", count=1
    )

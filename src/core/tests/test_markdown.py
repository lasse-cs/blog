import pytest

from django.core.exceptions import ImproperlyConfigured

from pytest_django.asserts import assertTemplateUsed, assertTemplateNotUsed

from core.test.factories import (
    MarkdownRoutablePageFactory,
    MarkdownViewablePageFactory,
    NoTemplateMarkdownPageFactory,
    NoTemplateMarkdownRoutablePageFactory,
)


pytestmark = [
    pytest.mark.django_db,
]


def test_returns_markdown_if_requested(client, site):
    markdown_page = MarkdownViewablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url, headers={"Accept": "text/markdown"})
    assert response.status_code == 200
    assert "text/markdown" in response.headers["Content-Type"]


def test_does_not_return_markdown_if_not_requested(client, site):
    markdown_page = MarkdownViewablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url)
    assert response.status_code == 200
    assert "text/markdown" not in response.headers["Content-Type"]


def test_uses_markdown_template_if_requested(client, site):
    markdown_page = MarkdownViewablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url, headers={"Accept": "text/markdown"})
    assertTemplateUsed(response, "test/markdown_page.md")
    assertTemplateNotUsed(response, "test/markdown_page.html")


def test_raises_if_no_markdown_template_provided(client, site):
    no_template_page = NoTemplateMarkdownPageFactory(
        parent=site.root_page, title="No template!"
    )
    with pytest.raises(ImproperlyConfigured):
        client.get(no_template_page.url, headers={"accept": "text/markdown"})


def test_adds_accept_into_vary_header(client, site):
    markdown_page = MarkdownViewablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url, headers={"accept": "text/markdown"})
    assert "Accept" in response.headers["Vary"]
    response = client.get(markdown_page.url)
    assert "Accept" in response.headers["Vary"]


def test_routable_returns_markdown_if_requested(client, site):
    markdown_page = MarkdownRoutablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url, headers={"Accept": "text/markdown"})
    assert response.status_code == 200
    assert "text/markdown" in response.headers["Content-Type"]


def test_routable_does_not_return_markdown_if_not_requested(client, site):
    markdown_page = MarkdownRoutablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url)
    assert response.status_code == 200
    assert "text/markdown" not in response.headers["Content-Type"]


def test_routable_uses_markdown_template_if_requested(client, site):
    markdown_page = MarkdownRoutablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url, headers={"accept": "text/markdown"})
    assertTemplateUsed(response, "test/markdown_page.md")
    assertTemplateNotUsed(response, "test/markdown_page.html")


def test_routable_raises_if_no_markdown_template_provided(client, site):
    no_template_page = NoTemplateMarkdownRoutablePageFactory(
        parent=site.root_page, title="No template!"
    )
    with pytest.raises(ImproperlyConfigured):
        client.get(no_template_page.url, headers={"accept": "text/markdown"})


def test_routable_adds_accept_into_vary_header(client, site):
    markdown_page = MarkdownRoutablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    response = client.get(markdown_page.url, headers={"accept": "text/markdown"})
    assert "Accept" in response.headers["Vary"]
    response = client.get(markdown_page.url)
    assert "Accept" in response.headers["Vary"]


def test_routable_page_route_not_opt_in_to_markdown(client, site):
    markdown_page = MarkdownRoutablePageFactory(
        parent=site.root_page, title="Markdown Page"
    )
    url = markdown_page.url + markdown_page.reverse_subpage("not-markdown")
    response = client.get(url, headers={"accept": "text/markdown"})
    assert "text/markdown" not in response.headers["Content-Type"]

import pytest

from pytest_django.asserts import assertTemplateUsed

from article.factories import ArticleIndexPageFactory, ArticlePageFactory
from article.models import ArticleIndexPage, ArticlePage


@pytest.fixture
def article_index(root_page):
    yield ArticleIndexPageFactory(parent=root_page)


@pytest.fixture
def article(article_index):
    yield ArticlePageFactory(parent=article_index)


def test_article_can_create_only_under_index():
    assert set(ArticlePage.allowed_parent_page_models()) == {ArticleIndexPage}


def test_article_can_not_have_children():
    assert not ArticlePage.allowed_subpage_models()


def test_article_index_can_only_have_article_children():
    assert set(ArticleIndexPage.allowed_subpage_models()) == {ArticlePage}


def test_article_page_summary_template():
    assert (
        ArticlePage.summary_template
        == "patterns/components/article/article_summary.html"
    )


@pytest.mark.django_db
def test_article_index_page_is_routable(client, article_index):
    response = client.get(article_index.url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_article_index_page_template(client, article_index):
    response = client.get(article_index.url)
    assertTemplateUsed(response, "patterns/pages/article/article_index_page.html")


@pytest.mark.django_db
def test_article_index_page_shows_live_articles(article_index):
    expected_ids = []
    for i in range(5):
        a = ArticlePageFactory(
            live=True, parent=article_index, title=f"live_article_{i}"
        )
        expected_ids.append(a.id)
    for j in range(2):
        ArticlePageFactory(
            live=False, parent=article_index, title=f"not_live_article_{j}"
        )
    assert set(a.id for a in article_index.get_feed_items()) == set(expected_ids)


@pytest.mark.django_db
def test_article_index_page_shows_summary_templates_for_each_article(
    client, article_index
):
    for i in range(5):
        ArticlePageFactory(parent=article_index, title=f"live_article_{i}")
    response = client.get(article_index.url)
    assertTemplateUsed(response, ArticlePage.summary_template, count=5)


@pytest.mark.django_db
def test_article_page_is_routable(client, article):
    response = client.get(article.url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_article_page_template(client, article):
    response = client.get(article.url)
    assertTemplateUsed(response, "patterns/pages/article/article_page.html")

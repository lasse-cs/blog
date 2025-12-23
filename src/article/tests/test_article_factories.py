import pytest

from wagtail.rich_text import RichText

from article.factories import ArticlePageFactory


@pytest.mark.django_db
def test_article_page_factory():
    article_page = ArticlePageFactory()
    assert article_page.intro == "Article intro content."


@pytest.mark.django_db
def test_article_page_factory_with_content():
    article_page = ArticlePageFactory(
        intro=RichText("<b>Hi There!</b>"), body__0__text="Hello There!"
    )
    assert article_page.intro == "<b>Hi There!</b>"
    assert len(article_page.body) == 1
    assert article_page.body[0].value == RichText("Hello There!")

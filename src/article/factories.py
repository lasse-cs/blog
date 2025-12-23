from wagtail_factories import PageFactory, StreamFieldFactory

from article.models import ArticleIndexPage, ArticlePage
from core.factories import ContentBlockFactory


class ArticleIndexPageFactory(PageFactory):
    class Meta:
        model = ArticleIndexPage


class ArticlePageFactory(PageFactory):
    body = StreamFieldFactory(ContentBlockFactory)

    class Meta:
        model = ArticlePage

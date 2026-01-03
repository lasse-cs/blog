from wagtail_factories import PageFactory, StreamFieldFactory

from article.models import ArticleIndexPage, ArticlePage
from core.factories import ContentBlockFactory, TaggablePageFactory


class ArticleIndexPageFactory(PageFactory):
    class Meta:
        model = ArticleIndexPage


class ArticlePageFactory(TaggablePageFactory):
    body = StreamFieldFactory(ContentBlockFactory)

    class Meta:
        model = ArticlePage

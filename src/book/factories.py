import factory
from factory.django import DjangoModelFactory

from wagtail_factories import PageFactory, ImageFactory

from book.models import Author, BookAuthor, BookIndexPage, BookPage


class AuthorFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Author


class BookIndexPageFactory(PageFactory):
    class Meta:
        model = BookIndexPage


class BookPageFactory(PageFactory):
    cover_image = factory.SubFactory(ImageFactory)
    progress = factory.Faker("random_int", min=0, max=100)

    class Meta:
        model = BookPage


class BookAuthorFactory(DjangoModelFactory):
    book = factory.SubFactory(BookPageFactory)
    author = factory.SubFactory(AuthorFactory)

    class Meta:
        model = BookAuthor


class BookPageWithAuthorFactory(BookPageFactory):
    author = factory.RelatedFactory(
        BookAuthorFactory, factory_related_name="book", sort_order=1
    )


class BookPageWithTwoAuthorsFactory(BookPageFactory):
    author1 = factory.RelatedFactory(
        BookAuthorFactory, factory_related_name="book", sort_order=1
    )
    author2 = factory.RelatedFactory(
        BookAuthorFactory, factory_related_name="book", sort_order=2
    )

import pytest
from pytest_django.asserts import assertTemplateUsed

from book.factories import BookIndexPageFactory, BookPageFactory
from book.models import BookIndexPage, BookPage


@pytest.fixture
def book_index_page(root_page):
    yield BookIndexPageFactory(parent=root_page, title="Book Index Page")


def test_book_page_has_no_children():
    assert not BookPage.allowed_subpage_models()


def test_book_page_summary_template():
    assert BookPage.summary_template == "patterns/components/book/book_summary.html"


def test_book_page_can_live_under_index():
    assert set(BookPage.allowed_parent_page_models()) == {BookIndexPage}


def test_book_index_page_can_only_have_book_children():
    assert set(BookIndexPage.allowed_subpage_models()) == {BookPage}


@pytest.mark.django_db
def test_book_index_page_can_be_rendered(client, book_index_page):
    response = client.get(book_index_page.url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_index_page_template(client, book_index_page):
    response = client.get(book_index_page.url)
    assertTemplateUsed(response, "patterns/pages/book/book_index_page.html")


@pytest.mark.django_db
def test_book_page_can_be_rendered(client, book_index_page):
    book_page = BookPageFactory(parent=book_index_page)
    response = client.get(book_page.url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_page_template(client, book_index_page):
    book_page = BookPageFactory(parent=book_index_page)
    response = client.get(book_page.url)
    assertTemplateUsed(response, "patterns/pages/book/book_page.html")

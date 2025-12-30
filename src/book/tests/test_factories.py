import pytest

from book.factories import BookPageWithAuthorFactory, BookNoteFactory


@pytest.mark.django_db
def test_book_page_with_notes(root_page):
    book_page = BookPageWithAuthorFactory(parent=root_page)
    BookNoteFactory.create_batch(size=2, book=book_page)
    assert len(book_page.book_notes.all()) == 2

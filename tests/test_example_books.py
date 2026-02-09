
import pytest
from books.models import Book

@pytest.mark.django_db
def test_book_creation():
    book = Book.objects.create(
        title="Example",
        author="Author",
        published_year=2026,
    )
    assert str(book) == "Example"

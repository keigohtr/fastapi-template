from datetime import datetime

import pytest

from app import entities


def test_bookcreate_happycase() -> None:
    title = "title"
    entry = entities.BookCreate(title=title)
    assert entry.title == title


def test_bookcreate_invalid() -> None:
    with pytest.raises(ValueError):
        entities.BookCreate()

    title = ""
    with pytest.raises(ValueError):
        entities.BookCreate(title=title)

    title = "." * 513
    with pytest.raises(ValueError):
        entities.BookCreate(title=title)


def test_book_happycase() -> None:
    book_id = "123456789012"
    title = "title"
    created_at = updated_at = datetime.utcnow()
    entry = entities.Book(book_id=book_id, title=title, created_at=created_at, updated_at=updated_at)
    assert entry.book_id == book_id
    assert entry.title == title
    assert entry.created_at == created_at
    assert entry.updated_at == updated_at


def test_book_invalid() -> None:
    book_id = "123456789012"
    title = "title"
    created_at = updated_at = datetime.utcnow()

    with pytest.raises(ValueError):
        entities.Book(title=title, created_at=created_at, updated_at=updated_at)

    with pytest.raises(ValueError):
        entities.Book(book_id=book_id, created_at=created_at, updated_at=updated_at)

    with pytest.raises(ValueError):
        entities.Book(book_id=book_id, title=title, updated_at=updated_at)

    with pytest.raises(ValueError):
        entities.Book(book_id=book_id, title=title, created_at=created_at)


def test_books_happycase() -> None:
    book_id = "123456789012"
    title = "title"
    created_at = updated_at = datetime.utcnow()
    entry = entities.Book(book_id=book_id, title=title, created_at=created_at, updated_at=updated_at)
    entries = [entry]
    books = entities.Books(entries=entries)
    assert books.entries is not None
    assert len(books.entries) == 1

    books = entities.Books(entries=[])
    assert books.entries is not None
    assert len(books.entries) == 0


def test_books_invalid() -> None:
    with pytest.raises(ValueError):
        entities.Books()

import pytest
from sqlalchemy.orm import Session

from app.entities import BookCreate
from app.exceptions import EntityNotFoundException, InvalidInputException
from app.services.book_service import BookService
from tests.utils.create_resources import create_random_book


def test_create_book_happycase(book_service: BookService, function_db: Session) -> None:
    title = "title"
    entry = BookCreate(title=title)
    response = book_service.create_book(db=function_db, entry=entry)
    assert response.book_id is not None
    assert response.title == title
    assert response.created_at is not None
    assert response.updated_at is not None


def test_list_books_happycase(book_service: BookService, function_db: Session) -> None:
    create_random_book(function_db, title="book1")
    create_random_book(function_db, title="book2")

    response = book_service.list_books(function_db, limit=10, offset=0)
    assert len(response) == 2

    response = book_service.list_books(function_db, limit=1, offset=0)
    assert len(response) == 1
    book_id = response[0].book_id
    response = book_service.list_books(function_db, limit=1, offset=1)
    assert len(response) == 1
    assert book_id != response[0].book_id

    response = book_service.list_books(function_db, limit=10, offset=2)
    assert len(response) == 0


def test_list_books_invalid(book_service: BookService, function_db: Session) -> None:
    create_random_book(function_db, title="book1")
    create_random_book(function_db, title="book2")

    with pytest.raises(InvalidInputException):
        book_service.list_books(function_db, limit=-1, offset=0)

    with pytest.raises(InvalidInputException):
        book_service.list_books(function_db, limit=10, offset=-1)


def test_fetch_book_happycase(book_service: BookService, function_db: Session) -> None:
    book = create_random_book(function_db)

    response = book_service.fetch_book(function_db, book_id=book.book_id)
    assert response.book_id == book.book_id
    assert response.title == book.title


def test_fetch_book_invalid(book_service: BookService, function_db: Session) -> None:
    create_random_book(function_db)

    with pytest.raises(EntityNotFoundException):
        book_service.fetch_book(function_db, book_id="noexist")

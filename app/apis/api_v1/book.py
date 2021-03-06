"""
Book API
"""
from typing import Any

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app import entities
from app.apis.utils import set_error_responses
from app.db import session
from app.services.book_service import BookService


def create_book_router(book_service: BookService) -> APIRouter:
    router = APIRouter()

    @router.post("", response_model=entities.Book, responses=set_error_responses([422]))
    async def create_book(
        *,
        db: Session = Depends(session.get_db),
        request_body: entities.BookCreate,
    ) -> Any:
        """POST /books

        Args:
            db (Session, optional): DB session.
            request_body (entities.BookCreate): Parameters to create Book.

        Returns:
            entities.Book: Book.
        """
        book = book_service.create_book(db, request_body)
        return entities.Book.create_from_model(book)

    @router.get("", response_model=entities.Books, responses=set_error_responses([422]))
    async def list_books(
        *,
        db: Session = Depends(session.get_db),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
    ) -> Any:
        """GET /books

        Args:
            db (Session, optional): DB session.
            limit (Optional[int], optional): Number of entries. Defaults to Query(10, ge=1, le=100).
            offset (Optional[int], optional): Offset for pagination. Defaults to Query(0, ge=0).

        Returns:
            entities.Books: List of books.
        """
        books = book_service.list_books(db, limit=limit, offset=offset)
        return entities.Books.create_from_model(books)

    @router.get("/{book_id}", response_model=entities.Book, responses=set_error_responses([404, 422]))
    async def fetch_book(
        *,
        db: Session = Depends(session.get_db),
        book_id: str = Path(..., min_length=1, max_length=36),
    ) -> Any:
        """GET /books/{book_id}

        Args:
            db (Session, optional): DB session.
            book_id (str, optional): Book ID. Defaults to Path(..., min_length=1, max_length=36).

        Returns:
            entities.Book: Book.
        """
        book = book_service.fetch_book(db, book_id=book_id)
        return entities.Book.create_from_model(book)

    return router

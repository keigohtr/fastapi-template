"""
Book entity.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.db import models


class BookBase(BaseModel):
    title: Optional[str] = None


class BookCreate(BookBase):
    title: str = Field(..., min_length=1, max_length=512)


class Book(BookBase):
    book_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_from_model(cls, book: models.Books) -> "Book":
        return cls(
            book_id=book.book_id,
            title=book.title,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )


class Books(BaseModel):
    entries: List[Book]

    @classmethod
    def create_from_model(cls, books: List[models.Books]) -> "Books":
        entries = [Book.create_from_model(x) for x in books]
        return cls(
            entries=entries,
        )

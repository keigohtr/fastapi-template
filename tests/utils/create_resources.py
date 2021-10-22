"""
Create test resources.
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import Books
from app.utils import random_resource_id


def create_random_book(db: Session, title: Optional[str] = "title") -> Books:
    book_id = random_resource_id()
    book = Books(book_id=book_id, title=title)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

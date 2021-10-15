"""
Book entity.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: Optional[str] = None


class BookCreate(BookBase):
    title: str = Field(..., min_length=1, max_length=512)


class Book(BookBase):
    book_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class Books(BaseModel):
    entries: List[Book]

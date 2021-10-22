"""
Book model.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from app.db.base_class import Base


class Books(Base):
    book_id = Column(String(36), primary_key=True, nullable=False)

    title = Column(String(512), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

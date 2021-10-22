"""
API Router
"""
from fastapi import APIRouter

from app.apis.api_v1.book import create_book_router
from app.services.book_service import BookService


def v1_router(book_service: BookService) -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(
        create_book_router(book_service),
        prefix="/books",
        tags=["books"],
    )
    return api_router

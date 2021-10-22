"""
Health check
"""
from typing import Any

from fastapi import APIRouter

from app import entities
from app.entities.message import MessageCodeEnum

router = APIRouter()


@router.get("/", response_model=entities.Message, include_in_schema=False)
@router.get("/health", response_model=entities.Message)
def health() -> Any:
    """Health check
    Returns:
        entities.Message: message.
    """
    return entities.Message(code=MessageCodeEnum.OK, message="ok")

"""
Exceptions.
"""

from fastapi import status

from app.entities.message import MessageCodeEnum


class ApiError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    code = MessageCodeEnum.BAD_REQUEST


class InvalidInputException(ApiError):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = MessageCodeEnum.UNPROCESSABLE_ENTITY


class EntityNotFoundException(ApiError):
    status_code: int = status.HTTP_404_NOT_FOUND
    code = MessageCodeEnum.NOT_FOUND

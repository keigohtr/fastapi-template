"""
Message entity.
"""
import enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class MessageCodeEnum(enum.Enum):
    OK = "OK"
    NOT_FOUND = "NOT_FOUND"
    UNPROCESSABLE_ENTITY = "UNPROCESSABLE_ENTITY"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class Message(BaseModel):
    code: MessageCodeEnum
    message: str
    detail: Optional[Union[Dict, List]]

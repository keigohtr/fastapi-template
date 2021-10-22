import pytest

from app import entities
from app.entities.message import MessageCodeEnum


def test_message_happycase() -> None:
    code = MessageCodeEnum.OK
    message = "ok"
    detail = {"key": "value"}
    entry = entities.Message(code=code, message=message, detail=detail)
    assert entry.code == code
    assert entry.message == message
    assert entry.detail == detail

    detail = [1, 2, 3]
    entry = entities.Message(code=code, message=message, detail=detail)
    assert entry.detail == detail


def test_message_invalid() -> None:
    code = MessageCodeEnum.OK
    message = "ok"
    detail = {"key": "value"}
    with pytest.raises(ValueError):
        entities.Message(code=code)

    with pytest.raises(ValueError):
        entities.Message(message=message)

    with pytest.raises(ValueError):
        entities.Message(code=code, message=message, detail="test")

    with pytest.raises(ValueError):
        entities.Message(code="dummy", message=message, detail=detail)

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app import entities
from tests.utils.create_resources import create_random_book


@pytest.mark.asyncio
async def test_create_book_happycase(client: AsyncClient) -> None:
    headers = {"x-requester": "dummy"}
    request_body = entities.BookCreate(title="title")

    response = await client.post("/v1/books", headers=headers, json=request_body.dict())
    assert response.status_code == 200
    response_body = response.json()
    assert response_body is not None
    assert "book_id" in response_body
    assert response_body["book_id"] is not None
    assert "title" in response_body
    assert response_body["title"] == "title"
    assert "created_at" in response_body
    assert response_body["created_at"] is not None
    assert "updated_at" in response_body
    assert response_body["updated_at"] is not None


@pytest.mark.asyncio
async def test_create_book_invalid(client: AsyncClient) -> None:
    headers = {"x-requester": "dummy"}
    request_body = {}

    response = await client.post("/v1/books", headers=headers, json=request_body)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_books_happycase(client: AsyncClient, session_db: Session) -> None:
    create_random_book(session_db, title="book1")
    create_random_book(session_db, title="book2")

    headers = {"x-requester": "dummy"}
    params = {"limit": 10, "offset": 0}
    response = await client.get("/v1/books", headers=headers, params=params)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body is not None
    assert "entries" in response_body
    assert len(response_body["entries"]) == 2

    params = {"limit": 1, "offset": 0}
    response = await client.get("/v1/books", headers=headers, params=params)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body is not None
    assert "entries" in response_body
    assert len(response_body["entries"]) == 1
    book = response_body["entries"][0]["book_id"]

    params = {"limit": 1, "offset": 1}
    response = await client.get("/v1/books", headers=headers, params=params)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body is not None
    assert "entries" in response_body
    assert len(response_body["entries"]) == 1
    assert book != response_body["entries"][0]["book_id"]


@pytest.mark.asyncio
async def test_list_books_invalid(client: AsyncClient, session_db: Session) -> None:
    create_random_book(session_db, title="book1")
    create_random_book(session_db, title="book2")

    headers = {"x-requester": "dummy"}
    params = {"limit": 0, "offset": 0}
    response = await client.get("/v1/books", headers=headers, params=params)
    assert response.status_code == 422

    params = {"limit": 101, "offset": 0}
    response = await client.get("/v1/books", headers=headers, params=params)
    assert response.status_code == 422

    params = {"limit": 10, "offset": -1}
    response = await client.get("/v1/books", headers=headers, params=params)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_fetch_book_happycase(client: AsyncClient, session_db: Session) -> None:
    book1 = create_random_book(session_db, title="book1")
    book2 = create_random_book(session_db, title="book2")

    headers = {"x-requester": "dummy"}
    response = await client.get(f"/v1/books/{book1.book_id}", headers=headers)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body is not None
    assert "book_id" in response_body
    assert response_body["book_id"] == book1.book_id

    response = await client.get(f"/v1/books/{book2.book_id}", headers=headers)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body is not None
    assert "book_id" in response_body
    assert response_body["book_id"] == book2.book_id


@pytest.mark.asyncio
async def test_fetch_book_invalid(client: AsyncClient, session_db: Session) -> None:
    create_random_book(session_db, title="book1")

    headers = {"x-requester": "dummy"}
    response = await client.get("/v1/books/noexist", headers=headers)
    assert response.status_code == 404

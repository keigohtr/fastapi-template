import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"code": "OK", "message": "ok", "detail": None}

    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"code": "OK", "message": "ok", "detail": None}

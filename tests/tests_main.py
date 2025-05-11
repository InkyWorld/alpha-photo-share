import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_app_startup():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/general/health_checker")
    assert response.status_code == 200
    assert response.json()["message"] == "Database is connected and healthy"
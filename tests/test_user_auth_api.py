import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_signup():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.post("/api/auth/signup", json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
            "age": 25,
            "gender": "M"
        })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.post("/api/auth/login", data={
            "username": "test@example.com",
            "password": "password123"
        })
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_refresh_token():
    async with AsyncClient(base_url="http://test") as ac:
        login_response = await ac.post("/api/auth/login", data={
            "username": "test@example.com",
            "password": "password123"
        })
        refresh_token = login_response.json()["refresh_token"]
        response = await ac.get("/api/auth/refresh_token", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
import pytest
from httpx import AsyncClient
from main import app
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_create_post():
    with TestClient(app) as test_app:
        async with AsyncClient(base_url="http://localhost:8000") as ac:
            response = await ac.post("/api/posts/", data={
                "title": "Test Post",
                "description": "This is a test post",
                "tags": ["test", "post"]
            })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_posts():
    with TestClient(app) as test_app:
        async with AsyncClient(base_url="http://localhost:8000") as ac:
            response = await ac.get("/api/posts/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_post():
    with TestClient(app) as test_app:
        async with AsyncClient(base_url="http://localhost:8000") as ac:
            response = await ac.patch("/api/posts/{post_id}", json={"title": "Updated Title"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_post():
    with TestClient(app) as test_app:
        async with AsyncClient(base_url="http://localhost:8000") as ac:
            response = await ac.delete("/api/posts/{post_id}")
    assert response.status_code == 204
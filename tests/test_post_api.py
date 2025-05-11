import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/posts/", data={
            "title": "Test Post",
            "description": "This is a test post",
            "tags": ["test", "post"]
        })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_posts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/posts/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch("/api/posts/{post_id}", json={"title": "Updated Title"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/api/posts/{post_id}")
    assert response.status_code == 204
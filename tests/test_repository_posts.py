import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.posts import create_post, get_post

@pytest.mark.asyncio
async def test_create_post(db_session: AsyncSession):
    post = await create_post(
        title="Test Post",
        description="This is a test post",
        image_url="http://example.com/image.jpg",
        user_id="123e4567-e89b-12d3-a456-426614174000",
        db=db_session
    )
    assert post.title == "Test Post"

@pytest.mark.asyncio
async def test_get_post(db_session: AsyncSession):
    post = await get_post("123e4567-e89b-12d3-a456-426614174000", db_session)
    assert post is not None
    assert post.title == "Test Post"
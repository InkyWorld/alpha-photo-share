import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user import get_user_by_email, create_user
from src.schemas.user import UserCreationSchema

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    user_data = UserCreationSchema(
        email="test@example.com",
        password="password123",
        full_name="Test User",
        age=25,
        gender="M"
    )
    user = await create_user(user_data, db_session)
    assert user.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession):
    user = await get_user_by_email("test@example.com", db_session)
    assert user is not None
    assert user.email == "test@example.com"
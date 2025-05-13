import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from src.repository.user import get_user_by_email, create_user
from src.schemas.user import UserCreationSchema
from src.models.users import User

@pytest.fixture
def db_session() -> AsyncSession:
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_user = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email="test@example.com",
        full_name="Test User",
        password="hashedpassword",  # Updated to match the User model
        age=25,
        gender="M"
    )
    mock_result.unique.return_value.scalar_one_or_none.return_value = mock_user  # Return a valid User object
    mock_session.execute.return_value = mock_result
    return mock_session

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
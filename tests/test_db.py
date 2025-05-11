import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import sessionmanager

@pytest.mark.asyncio
async def test_db_session():
    async with sessionmanager.session() as session:
        assert isinstance(session, AsyncSession)
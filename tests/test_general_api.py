import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.api.general.check import health_checker
from src.db.redis import get_redis
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Correct the lifespan override for testing
@asynccontextmanager
async def mock_lifespan(app):
    yield

app.lifespan = mock_lifespan

# Mock database session
logger.debug("Setting up mock database session")
mock_result = MagicMock()
mock_result.fetchone.return_value = (1,)
mock_session = AsyncMock(spec=AsyncSession)
mock_session.execute.return_value = mock_result
logger.debug("Mock database session setup complete")
app.dependency_overrides["get_db"] = lambda: mock_session

# Mock Redis manager
logger.debug("Setting up mock Redis manager")
mock_redis = AsyncMock()
mock_redis.ping.return_value = True
logger.debug("Mock Redis manager setup complete")
app.dependency_overrides["redis_manager"] = lambda: mock_redis

# Mock Redis session method
mock_redis_session = AsyncMock()
mock_redis_session.__aenter__.return_value = mock_redis
mock_redis_session.__aexit__.return_value = None

with patch("src.db.redis.redis_manager.session", return_value=mock_redis_session):
    app.dependency_overrides[get_redis] = lambda: mock_redis

# Mock HTTP requests
app.dependency_overrides["http_client"] = lambda: AsyncMock()

@pytest.mark.asyncio
async def test_health_checker():
    """
    Test the health checker endpoint.
    """
    with TestClient(app) as client:
        response = client.get("/api/general/health_checker")
        assert response.status_code == 200
        assert response.json() == {"message": "Database is connected and healthy", "result": 1}

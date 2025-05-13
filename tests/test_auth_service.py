import pytest
from src.services.auth import auth_service

@pytest.mark.asyncio
async def test_password_hashing():
    password = "password123"
    hashed = auth_service.get_password_hash(password)
    assert auth_service.verify_password(password, hashed)

@pytest.mark.asyncio 
async def test_token_creation():
    data = {"sub": "test@example.com"}
    token = await auth_service.create_access_token(data)
    assert token is not None

@pytest.mark.asyncio
async def test_token_decoding():
    data = {"sub": "test@example.com"}
    token = await auth_service.create_access_token(data)
    decoded = auth_service._decode_token(token, expected_scope="access_token")
    assert decoded["sub"] == "test@example.com"
import pytest
from src.services.roles import RoleAccessService
from src.models.users import Role, User
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_role_access():
    service = RoleAccessService(allowed_roles=[Role.admin])
    user = User(role=Role.admin)
    result = await service(None, user)
    assert result == user

@pytest.mark.asyncio
async def test_role_access_denied():
    service = RoleAccessService(allowed_roles=[Role.admin])
    user = User(role=Role.user)
    with pytest.raises(HTTPException):
        await service(None, user)
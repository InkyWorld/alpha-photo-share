from fastapi import Request, Depends, HTTPException, status

from src.models.users import Role, User
from src.core import log
from src.services.auth import auth_service


class RoleAccessService:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(
            self, request: Request, user: User = Depends(auth_service.authenticate_user)
    ):
        if user.role not in self.allowed_roles:
            log.debug(f"User {user.role} is not allowed")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN"
            )
        return user

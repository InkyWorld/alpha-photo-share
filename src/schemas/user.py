from abc import ABC
from typing import Annotated


from pydantic import BaseModel, Field, EmailStr, HttpUrl

from src.models.users import Role, Gender


class UserResponseSchema(BaseModel):
    password: Annotated[str, Field(min_length=6, max_length=255)]
    full_name: Annotated[str, Field(min_length=6, max_length=255)]
    email: EmailStr
    role: Role
    age: int
    gender: Gender


class UserCreationSchema(BaseModel):
    password: Annotated[str, Field(min_length=6, max_length=255)]
    full_name: Annotated[str, Field(min_length=6, max_length=255)]
    email: EmailStr
    age: int
    gender: Gender
    

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


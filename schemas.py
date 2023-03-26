# Pydantic models

from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]


class UserCreate(BaseModel):
    username: str
    gh_id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    roles: Role = Role['user']


class User(UserCreate):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str

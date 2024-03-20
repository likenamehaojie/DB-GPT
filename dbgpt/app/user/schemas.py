from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str = Field(..., description="", type="string")
    refresh_token: str = Field(..., description="", type="string")


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    user_ids: Optional[List] = None
    """page: page"""
    page: int = 1
    """page_size: page size"""
    page_size: int = 20


class UserOut(BaseModel):
    id: int
    email: str
    code: str = 200


class SystemUser(UserOut):
    password: str


class UserQueryResponse(BaseModel):
    """data: data"""

    data: List = None
    """total: total size"""
    total: int = None
    """page: current page"""
    page: int = None

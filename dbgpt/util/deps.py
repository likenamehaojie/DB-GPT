from typing import Union, Any, Optional
from datetime import datetime
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from dbgpt.app.openapi.api_view_model import Result
from pydantic import ValidationError

from dbgpt.app.user.schemas import SystemUser, TokenPayload, UserAuth, UserOut
from dbgpt.app.user.service import UserService
from dbgpt.serve.core import Result
from dbgpt.util.jwt_utils import JWT_SECRET_KEY, ALGORITHM
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Header(...)) -> UserOut:
    try:
        if token is None:
            Result.failed(code="E000X", msg=f"Token expired")

        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_service = UserService()
    user_auth = UserAuth(email=token_data.sub,password="00000")
    user = user_service.get_users(user_auth)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    user_out = UserOut(id=user.data[0].id,email=user.data[0].email)
    return user_out
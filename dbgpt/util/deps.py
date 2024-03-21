from typing import Union, Any, Optional
from datetime import datetime

from fastapi import   status, Header
from jose import jwt

from pydantic import ValidationError

from dbgpt.app.user.schemas import  TokenPayload, UserAuth, UserOut
from dbgpt.app.user.service import UserService
from dbgpt.serve.core.schemas import AuthException
from dbgpt.util.jwt_utils import JWT_SECRET_KEY, ALGORITHM


async def get_current_user(token: str = Header(default="1")) -> UserOut:
    try:
        if token is None:
            raise AuthException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )

        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise AuthException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
    except (jwt.JWTError, ValidationError):
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user_service = UserService()
    user_auth = UserAuth(email=token_data.sub,password="00000")
    user = user_service.get_users(user_auth)

    if user is None:
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not find user",
        )
    user_out = UserOut(id=user.data[0].id,email=user.data[0].email)
    return user_out
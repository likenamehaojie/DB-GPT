from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from dbgpt._private.config import Config

CFG = Config()
ACCESS_TOKEN_EXPIRE_MINUTES = CFG.ACCESS_TOKEN_EXPIRE_MINUTES  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = CFG.REFRESH_TOKEN_EXPIRE_MINUTES  # 7 days
ALGORITHM = CFG.ALGORITHM
JWT_SECRET_KEY = CFG.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = CFG.JWT_REFRESH_SECRET_KEY
# ALGORITHM = "HS256"
# JWT_SECRET_KEY = "asdfsfadfasdf"  # should be kept secret
# JWT_REFRESH_SECRET_KEY = "asdfasdf222222222 "  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

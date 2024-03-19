import logging


from fastapi import APIRouter, File, Form, UploadFile, Depends
from fastapi.security import OAuth2PasswordRequestForm

from dbgpt._private.config import Config
from dbgpt.app.openapi.api_view_model import Result
from dbgpt.app.user.schemas import UserAuth, TokenSchema
from dbgpt.app.user.service import UserService
from dbgpt.app.user.user_db import UserEntity
from dbgpt.util.deps import get_current_user
from dbgpt.util.jwt_utils import get_hashed_password, verify_password, create_access_token, create_refresh_token

logger = logging.getLogger(__name__)

CFG = Config()
router = APIRouter()


user_service = UserService()

@router.post('/signup', summary="Create new user")
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = user_service.get_users(data)
    if len(user.data) > 0:
        Result.failed(code="E000X", msg=f"user is already registered")
    user = UserEntity()
    user.password = get_hashed_password(data.password)
    user.email = data.email
    user_service.create_user(user) # saving user to database
    return user
@router.get('/me', summary='Get details of currently logged in user',dependencies=[Depends(get_current_user)])
async def get_me():
    return None


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_auth = UserAuth(email=form_data.username, password=form_data.password)
    user = user_service.get_users(user_auth)
    if user is None:
        Result.failed(code="E000X", msg=f"Incorrect email or password")

    hashed_pass = user.data[0].password
    if not verify_password(form_data.password, hashed_pass):
        Result.failed(code="E000X", msg=f"Incorrect email or password")


    return {
        "access_token": create_access_token(user.data[0].email),
        "refresh_token": create_refresh_token(user.data[0].email),
    }
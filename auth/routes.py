from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.exceptions import *

from .schema import CurrentUserResponse, Token, User, UserLoginForm
from .services import (authenticate_user, create_token, encrypt_password,
                       get_current_user)

USERS: list[User] = []
PREFIX = "/auth"

router = APIRouter(
    prefix = PREFIX,
    tags = ['Authentication']
)

oauth_bearer = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/token")


@router.post('/create', response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
async def create_user(form_data: UserLoginForm):
    # check if user already exists
    for _user in USERS:
        if _user.username == form_data.username:
            raise UserExists
        
    # create an user from the form data
    user = User(
        username = form_data.username,
        password = encrypt_password(form_data.password)
    )

    # add to database
    USERS.append(user)

    return user.id


@router.post('/token', response_model=Token, status_code=status.HTTP_201_CREATED)
async def generate_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, USERS)
    token = create_token(user['username'], user['id'], expiry_minutes=30)
    return Token(access_token=token, token_type='bearer')


@router.get('/me', response_model=CurrentUserResponse)
async def whoami(token: Annotated[str, Depends(oauth_bearer)]):
    return get_current_user(token)

import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import OperationalError

from core.exceptions import *

from .database import create_tables
from .schema import Token, UserCredentials, Users
from .services import AuthOperations, DatabaseOperations


@asynccontextmanager
async def lifespan(_app):
    while True:
        try:
            # create the tables to the database
            await create_tables()
            break

        except OperationalError as e:
            # if unable to connect then then retry after 10 seconds
            print(e)
            await asyncio.sleep(10)

    yield


PREFIX = "/auth"

router = APIRouter(
    prefix = PREFIX,
    tags = ['Authentication'],
    lifespan=lifespan
)   

oauth_bearer = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/token")


@router.post('/create', response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
async def create_user(form_data: UserCredentials, db_ops: Annotated[DatabaseOperations, Depends()]):
    # check if user already exists
    found_user = await db_ops.search_user(form_data.username)
    if found_user:
        raise UserExists

    # create an user from the form data
    user = Users(
        username = form_data.username,
        password = AuthOperations.encrypt_password(form_data.password)
    )

    # add to database
    await db_ops.add_user(user)

    return user.id


@router.post('/token', response_model=Token, status_code=status.HTTP_201_CREATED)
async def generate_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_ops: Annotated[DatabaseOperations, Depends()]):
    # authenticate user
    auth_data = await AuthOperations.authenticate_user(
        username = form_data.username,
        plain_text_password = form_data.password,
        db_ops = db_ops
    )

    # use auth data to generate token
    token = AuthOperations.create_auth_token(auth_data)

    return token


@router.get('/me', response_class=PlainTextResponse)
async def whoami(token: Annotated[str, Depends(oauth_bearer)]):
    return AuthOperations.get_current_user(token)

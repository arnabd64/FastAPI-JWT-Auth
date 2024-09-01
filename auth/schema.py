from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field
from ulid import ULID

current_timestamp = lambda: datetime.now()
user_id_generator = lambda: ULID().hex

class UserLoginForm(BaseModel):

    username: str
    password: str


class CurrentUserResponse(BaseModel):

    id: str
    username: str


class User(BaseModel):

    id: Annotated[Optional[str], Field(default_factory=user_id_generator)]
    username: str
    password: str
    created_on: Annotated[Optional[datetime], Field(default_factory=current_timestamp)]


class Token(BaseModel):

    access_token: str
    token_type: str
from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from ulid import ULID

current_timestamp = lambda: datetime.now()
uid_generator = lambda: ULID().hex

class Users(SQLModel, table=True):
    __tablename__ = 'users'

    id: str = Field(default_factory=uid_generator, primary_key=True)
    username: str = Field(unique=True)
    password: str = Field()
    created_on: datetime = Field(default_factory=current_timestamp)

class UserCredentials(BaseModel):

    username: str
    password: str


class Token(BaseModel):

    access_token: str
    token_type: str
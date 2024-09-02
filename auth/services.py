import secrets
from datetime import datetime, timedelta
from typing import Annotated, Dict

import sqlmodel
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import *

from .database import get_session
from .schema import Token, UserCredentials, Users

SECRET_KEY = 'c115fc7565605b25e64a92907cb47936a6f03face30cfb1ea38b42ab659df7d5'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
EXPIRY_MINUTES = 30

class DatabaseOperations:

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session


    async def search_user(self, username: str):
        """
        Queries the database for a specified username
        and returns the user's id
        """
        # build the query
        query = (
            sqlmodel
            .select(Users.id)
            .filter(Users.username == username)
        )

        # execute the query
        results = await self.session.exec(query)
        results = results.first()

        # validate
        return False if results is None else True
    

    async def get_user_credentials(self, username: str):
        """
        Queries the database for user's credentials
        """
        # build the query
        query = (
            sqlmodel
            .select(Users.username, Users.password)
            .filter(Users.username == username)
        )

        # execute the query
        results = await self.session.exec(query)
        results = results.first()

        # validate
        if results is None:
            raise UserNotFound

        return UserCredentials(username=results[1], password=results[0])
    

    async def add_user(self, user: Users):
        """
        Adds an user to the database
        """
        try:
            self.session.add(user)
            await self.session.commit()

        except Exception as e:
            await self.session.rollback()
            print(str(e))


class AuthOperations:

    @staticmethod
    def encrypt_password(plain_text_password: str):
        """
        Encrypts a plain text password
        """
        return bcrypt_context.hash(plain_text_password)
    

    @staticmethod
    def verify_password(plain_text_password: str, hashed_password: str):
        """
        Matches the plain text password with the hashed password
        """
        return bcrypt_context.verify(plain_text_password, hashed_password)
    
    
    @staticmethod
    async def authenticate_user(username: str, plain_text_password: str, db_ops: DatabaseOperations):
        """
        Authenticates user credentials
        """
        # retrieve the user's credentials
        user_credentials = await db_ops.get_user_credentials(username)

        # validate password
        if not AuthOperations.verify_password(plain_text_password, user_credentials.password):
            raise InvalidCredentials
        
        return {
            'username': user_credentials.username,
            'auth_secret': secrets.token_hex(32),
        }

        
    @staticmethod
    def create_auth_token(encoding_data: Dict[str, str]):
        """
        Generates an JWT Token

        Arguments:
        ----------
        - `encoding_data`: A dict object that will be encoded in the token
        """
        encoding_data.update({'expiration': datetime.now() + timedelta(minutes=EXPIRY_MINUTES)})
        token = jwt.encode(encoding_data, SECRET_KEY, ALGORITHM)
        return Token(access_token=token, token_type='bearer')


    @staticmethod
    def get_current_user(token: str):
        """
        Obtains the username from JWT token
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
            username = payload.get('username')

            if username is None:
                raise UserNotAuthorized
            
        except JWTError:
            raise JWTTokenException
        
        return username

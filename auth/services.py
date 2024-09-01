from datetime import datetime, timedelta
from typing import Dict, List

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.exceptions import *

from .schema import CurrentUserResponse, User

SECRET_KEY = 'c115fc7565605b25e64a92907cb47936a6f03face30cfb1ea38b42ab659df7d5'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def encrypt_password(plain_text_password: str):
    """
    Encrypts a plain text password
    """
    return bcrypt_context.hash(plain_text_password)


def authenticate_user(username: str, plain_text_password: str, users: List[User]) -> Dict[str, str]:
    """
    Authenticates user credentials
    """
    # search for the user in the database
    found_user = False
    for user in users:
        if user.username == username:
            found_user = True
            break

    # user not found
    if not found_user:
        raise UserNotFound
    
    # password don't match
    if not bcrypt_context.verify(plain_text_password, user.password):
        raise InvalidCredentials
    
    return {
        'username': user.username,
        'id': user.id
    }


def create_token(username: str, user_id: str, expiry_minutes: int):
    content = {
        'username': username,
        'id': user_id,
        'exp': datetime.now() + timedelta(minutes=expiry_minutes)
    }
    return jwt.encode(content, SECRET_KEY, ALGORITHM)


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get('username')
        user_id = payload.get('id')
        expiry = payload.get('exp')

        if username is None or user_id is None:
            raise UserNotAuthorized
        
    except JWTError:
        raise JWTTokenException
    
    return CurrentUserResponse(id=user_id, username=username)

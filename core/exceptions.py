"""
module: exceptions

description:

contains all custom exceptions made for this
application.
"""
from fastapi.exceptions import HTTPException

UserNotFound = HTTPException(404, 'user found not')
UserNotAuthorized = HTTPException(401, 'unauthorized user')
UserExists = HTTPException(409, 'user already created')
InvalidCredentials = HTTPException(401, "invalid login credentials")
JWTTokenException = HTTPException(401, 'invalid bearer token')
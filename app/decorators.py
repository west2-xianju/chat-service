from flask import abort, request
from app.utils import jwt_functions
from app.models import BaseResponse
import functools

# get bearer jwt token from http authorization header.
# verify it check if valid

def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return BaseResponse(code=401, message='No token').dict()

        token = request.headers.get('Authorization').split(' ')[1]
        payload = jwt_functions.verify_jwt(token)

        if not payload:
            return BaseResponse(code=401, message='invalid token').dict()

        return f(*args, **kwargs)
    return wrapper

from flask import request
from app.utils import jwt_functions
from app.models import BaseResponse
import functools
from flask_socketio import disconnect, emit

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
        
        
        new_kwargs = {'payload': payload}
        new_kwargs.update(kwargs)
        return f(*args, **new_kwargs)
    return wrapper

def token_required_socket(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('jwt')
        if not token:
            emit('status', {'msg': 'No token'})
            disconnect()
            
        payload = jwt_functions.verify_jwt(token)
        if not payload:
            emit('status', {'msg': 'invalid token'})
            disconnect()
            
        new_kwargs = {'payload': payload}
        new_kwargs.update(kwargs)
        return f(*args, **new_kwargs)
    return wrapper

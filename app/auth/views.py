from flask import request
from app.auth import auth
from app.models import BaseResponse

from app.utils import jwt_functions


@auth.route('/<int:user_id>', methods=['GET'])
def get_user_jwt(user_id):
    token = jwt_functions.generate_jwt({'user_id': user_id})
    
    detoken = jwt_functions.veryif_jwt(token)
    
    return BaseResponse(data={'token': token, 'result': detoken}).dict()


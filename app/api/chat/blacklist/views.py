from flask import redirect, request, url_for
from . import blacklist
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from .models import BlackList

from sqlalchemy import or_
from datetime import datetime

from snowflake import SnowflakeGenerator


@blacklist.route('/', methods=['GET'])
@login_required
def get_blacklist(payload: dict = {}):
    ret = BlackList.query.filter_by(user_id=payload['user_id']).all()
    
    return BaseResponse(data={'blacklist': [i.to_dict() for i in ret], 'count': len(ret)}).dict()

@blacklist.route('/<int:blocked_user_id>', methods=['POST'])
@login_required
def block_user(blocked_user_id, payload: dict = {}):
    if blocked_user_id == payload['user_id']:
        return BaseResponse(code=201, message="You can't block yourself").dict()
    
    result = BlackList(user_id=payload['user_id'], blocked_user_id=blocked_user_id).save()
    
    return BaseResponse(message='block user %d' % blocked_user_id, data=result.to_dict()).dict()


@blacklist.route('/<int:blocked_user_id>', methods=['DELETE'])
@login_required
def delete_block_user(blocked_user_id, payload: dict = {}):
    if blocked_user_id == payload['user_id']:
        return BaseResponse(code=400, message="You can't do it to yourself").dict()
    
    result = BlackList.query.filter_by(user_id=payload['user_id'], blocked_user_id=blocked_user_id).first()
    if not result:
        return BaseResponse(code=404, message="User requested wasn't blocked").dict()
    
    result.delete()
    
    return BaseResponse(message='unblock user %d' % blocked_user_id).dict()
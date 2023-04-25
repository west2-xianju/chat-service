from flask import redirect, request, url_for
from . import notifications
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from .models import Notification

from sqlalchemy import or_
from datetime import datetime

from snowflake import SnowflakeGenerator

from app.api import client_count

# @chat.route("/", methods=['GET', 'POST'])
# def index():
#     result = Message.query.filter_by(detail='hello').all()
#     mes = Message(room_id=1, sender_id=1, detail=request.json.get('username')).save()
#     # return {"all": [i.to_dict() for i in result]}
#     return BaseResponse(code=222, message='hi', data={"msg": [i.to_dict() for i in result]}).dict()


@notifications.route('/<int:goods_id>', methods=['POST'])
@login_required
def establish_room(goods_id):
    pass

@notifications.route('/', methods=['GET'])
@login_required
def pull_notification(room_id):
    payload = jwt_functions.verify_jwt(request.headers.get('Authorization').split(' ')[1])
    
    notification_list = Notification.query.filter_by(receiver_id=payload['user_id']).all()
    response_dict = {'notification_list': [i.to_dict() for i in notification_list]}
    
    for _ in notification_list:
        _.delete()
    
    return BaseResponse(data=response_dict).dict()


@notifications.route('/', methods=['GET'])
@login_required
def get_chat_list():
    pass
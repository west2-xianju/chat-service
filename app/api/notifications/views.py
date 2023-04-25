from flask import redirect, request, url_for
from . import notifications
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from .models import Notification

from sqlalchemy import or_
from datetime import datetime

from snowflake import SnowflakeGenerator

from app.api import client_counter

from app.api.chat.models import Room

from . import generate_notification_roomid


@notifications.route('/', methods=['POST'])
@login_required
def establish_notification_room():
    payload = jwt_functions.verify_jwt(request.headers.get('Authorization').split(' ')[1])
    
    # snow_gen = SnowflakeGenerator(2)
    notification_room_id = generate_notification_roomid(payload['user_id'])
    Room(room_id=notification_room_id, seller_id=payload['user_id']).save()
    
    return BaseResponse(data={'room_id': notification_room_id}).dict()

@notifications.route('/', methods=['GET'])
@login_required
def pull_notification():
    payload = jwt_functions.verify_jwt(request.headers.get('Authorization').split(' ')[1])
    
    notification_list = Notification.query.filter_by(user_id=payload['user_id']).all()
    response_dict = {'notification_list': [i.to_dict() for i in notification_list]}
    
    for _ in notification_list:
        _.delete()
    
    return BaseResponse(data=response_dict).dict()


@notifications.route('/', methods=['GET'])
@login_required
def get_chat_list():
    pass

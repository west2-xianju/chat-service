from flask import redirect, request, url_for
from . import notifications
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from .models import Notification
from .schemas import NotificationBase

from sqlalchemy import or_
from datetime import datetime
from app import socketio
import json

from snowflake import SnowflakeGenerator

from ..chat.models import Room
from app import client_manager


from . import generate_notification_roomID


# @notifications.route('/', methods=['POST'])
# @login_required
# def establish_notification_room(payload: dict = {}):
#     snow_gen = SnowflakeGenerator(instance=1)
#     notification_room_id = generate_notification_roomID(payload['user_id'])
#     Room(room_id=notification_room_id, seller_id=payload['user_id']).save()
    
#     return BaseResponse(data={'room_id': notification_room_id}).dict()


# TODO
# save notifications into redis db
@notifications.route('/', methods=['GET'])
@login_required
def pull_notification(payload: dict = {}):
    notification_list = Notification.query.filter_by(user_id=payload['user_id']).all()
    response_dict = {'notifications': [i.to_dict() for i in notification_list], 'count': len(notification_list)}
    
    for _ in notification_list:
        _.delete()
    
    return BaseResponse(data=response_dict).dict()


@notifications.route('/<int:user_id>', methods=['POST'])
def push_notification(user_id):
    if not request.data:
        return BaseResponse(code=400, message='bad request').dict()
    
    notificationObj = NotificationBase(**json.loads(request.data))
    
    # check if user online 
    if client_manager.check_user_if_online(user_id):
        # if online, push notification to client
        # if not, save notification to database
        
        call_push(notificationObj.dict(), generate_notification_roomID(user_id))
        # socketio.emit('notification', notificationObj.dict(), room=generate_notification_roomID(user_id), namespace='/notification')
        return BaseResponse(message='send', data=notificationObj.dict()).dict()
    else:
        Notification(user_id=user_id, **notificationObj.dict()).save()
        return BaseResponse(code=201, message=f'user {user_id} is not online').dict()
    
    return BaseResponse(message='unknown error').dict()


def call_push(notificationObject, room):
    socketio.emit('notification', notificationObject, room=room, namespace='/notification')
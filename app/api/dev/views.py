from flask import redirect, request, url_for
from . import dev
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from ..chat.models import Message, Room, Goods

from app.api import client_count
from flask_socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from app.api.notifications import notification_room_generator
from app.api.notifications.models import Notification

from app import socketio
import json

@dev.route('/chat', methods=['GET'])
def get_online_clients_count():
    
    return BaseResponse(code=client_count.get()).dict()



@dev.route('/chat/<int:sender_id>', methods=['PUT'])
def gen_message(sender_id):
    ret = Message(room_id=request.json.get('room_id'),
                  sender_id=sender_id,
                  detail=request.json.get('detail'),
                  send_time=request.json.get('send_time')).save()
    
    return BaseResponse(data=ret.to_dict()).dict()

@dev.route('/room/<int:room_id>', methods=['PUT'])
def gen_room(room_id):
    ret = Room(room_id=room_id,
               seller_id=request.json.get('seller_id'),
               goods_id=request.json.get('goods_id'),
               buyer_id=request.json.get('buyer_id')).save()
    
    return BaseResponse(data=ret.to_dict()).dict()



@dev.route('/auth/<int:user_id>', methods=['GET'])
def get_user_jwt(user_id):
    token = jwt_functions.generate_jwt({'user_id': user_id})
    

    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()


@dev.route('/notifications/<int:user_id>', methods=['POST'])
def push_notification(user_id):
    if not request.data:
        return BaseResponse(code=400, message='bad request').dict()
    
    data = json.loads(request.data)
    
    # check if user online 
    if client_count.is_online(user_id):
        # if online, push notification to client
        # if not, save notification to database
        
        socketio.emit('notification', data, room=notification_room_generator(user_id), namespace='/chat')
        return BaseResponse(message='send', data=data).dict()
    else:
        Notification(user_id=user_id, **data).save()
        return BaseResponse(message='user not online', data=data).dict()
    
    return BaseResponse(message='unknown error').dict()
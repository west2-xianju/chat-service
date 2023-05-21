from flask import redirect, request, url_for
from . import dev
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from ..chat.models import Message, Room, Good

from flask_socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from app.api.notifications import generate_notification_roomID
from app.api.notifications.models import Notification

from app import socketio, client_manager
import json


@dev.route('/clients', methods=['GET'])
def get_online_clients_count():
    
    return BaseResponse(data={'count': client_manager.get_user_count(), 'users': client_manager.USER_TABLE, 'sid_table': client_manager.SID_TABLE}).dict()



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
    token = jwt_functions.generate_jwt({'user_id': user_id, 'blocked': False})
    

    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()

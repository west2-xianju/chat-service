from flask import session, request, current_app
from flask_socketio import emit, join_room, leave_room, disconnect, rooms
from ... import socketio
from app.utils import jwt_functions
from app.decorators import token_required_socket
from .models import Room, Message

from datetime import datetime
from app import client_manager

import jwt
# TODO: use redis for client list maintaining, one user can only establish one connection

@socketio.on('connect', namespace='/chat')
def connect(message):
    emit('status', {'msg': 'Trying to connect to chat service, with following data: ', 'data': message})
    
    # Check if token is provided
    token = message['token']
    if token == None:
        emit('status', {'msg': 'Token is required. Disconnecting...'})
        disconnect()
        return
    
    # Check if token is valid
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        emit('status', {'msg': 'Token is invalid. Disconnecting...'})
        disconnect()
        return
    
    # Check if user is connected to notification service
    if not client_manager.check_user_if_online(payload['user_id']):
        emit('status', {'msg': 'You are not connected to notification service. Disconnecting...'})
        disconnect()
        return
    
    # join_room(room_id)
    client_manager.add_sid(payload['user_id'], request.sid)
    emit('status', {'msg': 'Connected to chat service'})


@socketio.event(namespace='/chat')
def join(message):
    user_id = client_manager.get_user_id_by_sid(request.sid)
    if user_id == None:
        emit('status', {'msg': 'You are not connected to chat service. Disconnecting...'})
        disconnect()
        return
    
    # Check if room_id is provided
    room_id = message['room_id']
    if room_id == None:
        emit('status', {'msg': 'Room id is required. Disconnecting...'})
        disconnect()
        return
    
    # Check if user if permitted to access the room
    room = Room.query.filter_by(room_id=room_id).first()
    if not room:
        emit('status', {'msg': 'Room not found. Disconnecting...'})
        disconnect()
        return

    if not (room.seller_id == user_id or room.buyer_id == user_id):
        emit('status', {'msg': 'You are not permitted to access this room. Disconnecting...'})
        disconnect()
        return
    
    join_room(room_id)
    client_manager.add_room(request.sid, room_id)
    emit('status', {'msg': 'Joined room {}'.format(room_id)})
    

@socketio.on('message', namespace='/chat')
def send_message(message):
    user_id = client_manager.get_user_id_by_sid(request.sid)
    if user_id == None:
        emit('status', {'msg': 'You are not connected to chat service. Disconnecting...'})
        disconnect()
        return
    room = client_manager.get_room_by_sid(request.sid)
    Message(room_id=room, sender_id=user_id, detail=message['detail'], send_time=datetime.utcnow(), type=message['type']).save()
    
    emit('message', {'sender': user_id, 'detail': message['detail'], 'send_time': datetime.utcnow().timestamp(), 'type': message['type']}, room=room, namespace='/chat')
    
@socketio.event(namespace='/chat')
def disconnect(): 
    client_manager.delete_room(request.sid)
    client_manager.delete_sid(request.sid)
    
    current_app.logger.debug('disconnected')
    emit('status', {'msg': 'Disconnected'})

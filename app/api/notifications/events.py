from flask import session, request, current_app
from flask_socketio import emit, join_room, leave_room, disconnect, rooms
from ... import socketio
from app.utils import jwt_functions
from app.decorators import token_required_socket

from app import client_manager
from . import generate_notification_roomID

import jwt
# TODO: use redis for client list maintaining, one user can only establish one connection

def token_verify_handler(token):
    if token == None:
        emit('status', {'msg': 'No token'})
        disconnect()
        return
    
    payload = jwt_functions.verify_jwt(token)
    if not payload:
        emit('status', {'msg': 'invalid token'})
        disconnect()
        return
    return payload

@socketio.on('connect', namespace='/notification')
def connect(message):
    emit('status', {'msg': 'Trying to connect to notification service, with following data: ', 'data': message})
    token = message['token']
    if token == None:
        emit('status', {'msg': 'Token is required. Disconnecting...'})
        disconnect()
        return
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        emit('status', {'msg': 'invalid token'})
        disconnect()
        return
    emit('status', {'msg': 'parse payload: ', 'data': payload})
    
    client_manager.connect(int(payload['user_id']), token, request.sid)
    current_app.logger.debug(
        'current user %d', client_manager.get_user_count())
    join_room(generate_notification_roomID(int(payload['user_id'])))
    
    emit('status', {'msg': 'Connected to notification service'})

@socketio.on('push', namespace='/notification')
def push_notification(message):
    user_id = client_manager.get_user_id_by_sid(request.sid)
    if user_id == None:
        emit('status', {'msg': 'You are not connected to notification service. Disconnecting...'})
        disconnect()
        return
    
    # Check if room_id is provided
    room_id = generate_notification_roomID(user_id)
    
    emit('notification', message)
    
@socketio.on('leave', namespace='/notification')
@token_required_socket
def leave(message, payload: dict = {}):
    user_id = int(payload['user_id'])
    
    client_manager.disconnect(user_id)
    client_manager.show_sid_table()
    
    current_app.logger.info('User %d log out notification', user_id)

@socketio.on('disconnect', namespace='/notification')
@token_required_socket
def logout(payload: dict = {}):
    user_id = client_manager.get_user_id_by_sid(request.sid)
    print(user_id)
    client_manager.disconnect(user_id)
    client_manager.show_sid_table()
    
    current_app.logger.debug('user %d lost notification connection.', user_id)

from flask import session, request, current_app
from flask_socketio import emit, join_room, leave_room, disconnect
from ... import socketio
from app.utils import jwt_functions
from app.decorators import token_required_socket
from .models import Room, Message

from app.api import client_count

# TODO: use redis for client list maintaining, one user can only establish one connection

@socketio.on('join', namespace='/chat')
@token_required_socket
def join(message):
    payload = jwt_functions.verify_jwt(session.get('token'))
    
    room = message['room_id']
    user_id = int(payload['user_id'])
    roomObj = Room.query.filter_by(room_id=room).first()
    # check if room exists
    if not roomObj:
        current_app.logger.info('User %d try to enter %d room. Not found.', user_id, room)
        emit('status', {'msg': 'Room does not exist.'})
        disconnect()
        return
    # check if permitted
    if roomObj.seller_id != user_id and roomObj.buyer_id != user_id:
        current_app.logger.info('User %d try to enter %d room. Rejected.', user_id, room)
        emit('status', {'msg': 'not allowed'})
        disconnect()
        return
    
    client_count.add_user(user_id, room)
    print(client_count.client_dict)
    current_app.logger.debug('current user %d', client_count.get())
    join_room(room)
    current_app.logger.info('User %d try to enter %d room. Allowed.', user_id, room)
    emit('status', {'msg': payload['user_id'] + ' has entered the room.'}, room=room)


@socketio.on('send', namespace='/chat')
@token_required_socket
def send(message):
    payload = jwt_functions.verify_jwt(session.get('token'))
    
    user_id = int(payload['user_id'])
    room = int(session.get('room_id'))
    
    Message(room_id=room, sender_id=payload['user_id'], detail=message['detail'], type=message['type']).save()
    current_app.logger.info('User %d send a message in room %d, which content is "%s"...', user_id, room, message['detail'][:10])
    emit('message', {'msg': f"{user_id}: {message['detail']}"}, room=room)


@socketio.on('leave', namespace='/chat')
@token_required_socket
def leave(message):
    payload = jwt_functions.verify_jwt(session.get('token'))
    
    user_id = int(payload['user_id'])
    room = int(session.get('room_id'))
    leave_room(room)
    current_app.logger.info('User %d left room %d', user_id, room)
    emit('status', {'msg': payload['user_id'] + ' has left the room.'}, room=room)


@socketio.on("disconnect",namespace='/chat')
@token_required_socket
def disconnect():
    payload = jwt_functions.verify_jwt(session.get('token'))
    
    print(client_count.client_dict)
    current_app.logger.info('somebody disconnected')
    
@socketio.on('logout', namespace='/chat')
@token_required_socket
def logout():
    payload = jwt_functions.verify_jwt(session.get('token'))
    user_id = int(payload['user_id'])
    
    client_count.log_out(user_id)
    print(client_count.client_dict)
    
    current_app.logger.debug('somebody logout, current user %d', client_count.get())
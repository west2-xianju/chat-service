from flask import session, request, current_app
from flask_socketio import emit, join_room, leave_room, disconnect, rooms
from .. import socketio
from app.utils import jwt_functions
from app.decorators import token_required_socket

from app import client_manager

@socketio.on('logout', namespace='/')
@token_required_socket
def logout(payload: dict = {}):
    user_id = int(payload['user_id'])

    client_manager.disconnect(user_id)
    client_manager.show_sid_table()

    current_app.logger.debug(
        'somebody logout, current user %d', client_manager.get_user_count())

from flask import redirect, request, url_for
from . import chat
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from .models import Message, Room, Good

from sqlalchemy import or_
from datetime import datetime

from snowflake import SnowflakeGenerator


@chat.route('/<int:goods_id>', methods=['POST'])
@login_required
def establish_room(goods_id, payload: dict = {}):
    # check if goods exist
    goods_info = Good.query.filter_by(good_id=goods_id).first()
    if not goods_info:
        return BaseResponse(code=404, message='goods not found').dict()
    
    # check if room exist
    # if not, create a new room
    # if yes, return the room id
    query_result = Room.query.filter_by(goods_id=goods_id, buyer_id=payload['user_id']).first()
    if query_result:
        return BaseResponse(code=201, message='room already existed', data={'room_id': query_result.room_id}).dict()
    
    id_gen = SnowflakeGenerator(1)
    result = Room(room_id=next(id_gen),
         seller_id=goods_info.seller_id,
         goods_id=goods_id,
         buyer_id=payload['user_id']).save()
    
    return BaseResponse(data=result.to_dict()).dict()

@chat.route('/log/<int:room_id>', methods=['GET'])
@login_required
def pull_message_logs(room_id, payload: dict = {}):
    start_time = datetime.utcfromtimestamp(0)
    end_time = datetime.utcnow()
    
    if request.args.get('start_time'):
        start_time = datetime.utcfromtimestamp(int(request.args.get('start_time')))
    if request.args.get('end_time'):
        end_time =  datetime.utcfromtimestamp(int(request.args.get('end_time')))
    # msg = Message.query.filter_by(room_id=room_id, sender_id=payload['user_id']).all()
    # msg = Message.query.filter(Message.send_time.between(start_time, end_time)).all()
    msg = Message.query.filter_by(room_id=room_id, sender_id=payload['user_id']).filter(Message.send_time.between(start_time, end_time)).all()
    return BaseResponse(data={'msg': [i.to_dict() for i in msg],
                              'create_time': datetime.isoformat(datetime.utcnow(), sep=' '),
                              'start_time': datetime.isoformat(start_time, sep=' '),
                              'end_time': end_time,
                              'room_id': room_id}).dict()

@chat.route('/', methods=['GET'])
@login_required
def get_chat_list(payload: dict = {}):
    # ret = Room.query.filter(Room.seller_id == payload['user_id']).all()
    room_list = Room.query.filter(or_(Room.seller_id == payload['user_id'], Room.buyer_id == payload['user_id'])).all()
    return BaseResponse(data={'room': [i.to_dict() for i in room_list]}).dict()


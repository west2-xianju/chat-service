from flask import redirect, request, url_for
from app.chat import chat
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from .models import Message, Room, Goods

from sqlalchemy import or_
from datetime import datetime

from snowflake import SnowflakeGenerator

# @chat.route("/", methods=['GET', 'POST'])
# def index():
#     result = Message.query.filter_by(detail='hello').all()
#     mes = Message(room_id=1, sender_id=1, detail=request.json.get('username')).save()
#     # return {"all": [i.to_dict() for i in result]}
#     return BaseResponse(code=222, message='hi', data={"msg": [i.to_dict() for i in result]}).dict()


@chat.route('/<int:sender_id>', methods=['PUT'])
def gen_message(sender_id):
    ret = Message(room_id=request.json.get('room_id'),
                  sender_id=sender_id,
                  detail=request.json.get('detail'),
                  send_time=request.json.get('send_time')).save()
    
    return BaseResponse(data=ret.to_dict()).dict()

@chat.route('/room/<int:room_id>', methods=['PUT'])
def gen_room(room_id):
    ret = Room(room_id=room_id,
               seller_id=request.json.get('seller_id'),
               goods_id=request.json.get('goods_id'),
               buyer_id=request.json.get('buyer_id')).save()
    
    return BaseResponse(data=ret.to_dict()).dict()


@chat.route('/<int:goods_id>', methods=['POST'])
@login_required
def establish_room(goods_id):
    payload = jwt_functions.verify_jwt(request.headers.get('Authorization').split(' ')[1])
    
    # check if goods exist
    goods_info = Goods.query.filter_by(uid=goods_id).first()
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
def pull_message_logs(room_id):
    payload = jwt_functions.verify_jwt(request.headers.get('Authorization').split(' ')[1])

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
                              'create_time': datetime.utcnow(),
                              'start_time': start_time,
                              'end_time': end_time,
                              'room_id': room_id}).dict()

@chat.route('/', methods=['GET'])
@login_required
def get_chat_list():
    payload = jwt_functions.verify_jwt(request.headers.get('Authorization').split(' ')[1])

    # ret = Room.query.filter(Room.seller_id == payload['user_id']).all()
    room_list = Room.query.filter(or_(Room.seller_id == payload['user_id'], Room.buyer_id == payload['user_id'])).all()
    return BaseResponse(data={'room': [i.to_dict() for i in room_list]}).dict()


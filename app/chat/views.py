from flask import redirect, request, url_for
from app.chat import chat
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions
from .models import Message, Room

from sqlalchemy import or_
from datetime import datetime

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
    return BaseResponse(data={'userid': payload['user_id']}).dict()

@chat.route('/log/<int:room_id>', methods=['GET'])
@login_required
def pull_message_logs(room_id):
    payload = jwt_functions.verify_jwt(request.headers.get('Authorization').split(' ')[1])

    start_time = 0
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
    ret = Room.query.filter(or_(Room.seller_id == payload['user_id'], Room.buyer_id == payload['user_id'])).all()
    return BaseResponse(data={'msg': [i.to_dict() for i in ret]}).dict()


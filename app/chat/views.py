from flask import redirect, request, url_for
from app.chat import chat
from app.models import BaseResponse
from .models import Message

@chat.route("/", methods=['GET', 'POST'])
def index():
    result = Message.query.filter_by(detail='hello').all()
    mes = Message(room_id=1, sender_id=1, detail=request.json.get('username')).save()
    # return {"all": [i.to_dict() for i in result]}
    return BaseResponse(code=222, message='hi', data={"msg": [i.to_dict() for i in result]}).dict()


@chat.route('/<int:goods_id>', methods=['POST'])
def establish_room(goods_id):
    return BaseResponse().dict()

@chat.route('/log/<int:room_id>', methods=['GET'])
def pull_message_logs(room_id):
    return BaseResponse().dict()

@chat.route('/', methods=['GET'])
def get_chat_list(room_id):
    return BaseResponse().dict()


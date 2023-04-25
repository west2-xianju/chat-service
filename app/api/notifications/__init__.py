from flask import Blueprint

notifications = Blueprint('notifications', __name__)


def notification_room_generator(user_id):
    return int(str(user_id) + '000' )

from . import views, models, events
from flask import Blueprint

notifications = Blueprint('notifications', __name__)

# TODO
# make room_id related to user_id, timestamp.
def generate_notification_roomID(user_id):
    return int(str(user_id) + '000' )

from . import views, models, events
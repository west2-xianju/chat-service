from flask import Blueprint

blacklist = Blueprint('blacklist', __name__)
from . import views, models

# def check_if_user_is_blacklisted(user_id):
#     return models.Blacklist.query.filter_by(user_id=user_id).first()

def check_if_blocked_user(user_id, blocked_user_id):
    if models.BlackList.query.filter_by(user_id=user_id, blocked_user_id=blocked_user_id).first():
        return True

    return False

def check_if_user_is_blocked(user_id, blocked_user_id):
    if models.BlackList.query.filter_by(user_id=blocked_user_id, blocked_user_id=user_id).first():
        return True
    
    return False

# from .. import client_manager
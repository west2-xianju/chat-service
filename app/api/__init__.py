

from .dev import dev as dev_blueprint
from .notifications import notifications as notification_blueprint
from .chat import chat as chat_blueprint
from .auth import auth as auth_blueprint
from flask import Blueprint
from ..utils.client_manager import ClientManager

from . import events


api = Blueprint('api', __name__)

api.register_blueprint(auth_blueprint, url_prefix='/auth')

api.register_blueprint(chat_blueprint, url_prefix='/chat')

api.register_blueprint(notification_blueprint, url_prefix='/notifications')

api.register_blueprint(dev_blueprint, url_prefix='/dev')

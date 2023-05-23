from flask import Blueprint

chat = Blueprint('chat', __name__)
from . import events, views, models

from .blacklist import blacklist as blacklist_blueprint
from .clients import clients as clients_blueprint
chat.register_blueprint(blacklist_blueprint, url_prefix='/blacklist')
chat.register_blueprint(clients_blueprint, url_prefix='/clients')

# from .. import client_manager

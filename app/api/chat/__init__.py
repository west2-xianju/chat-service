from flask import Blueprint

chat = Blueprint('chat', __name__)
from . import events, views, models

from .blacklist import blacklist as blacklist_blueprint

chat.register_blueprint(blacklist_blueprint, url_prefix='/blacklist')

# from .. import client_manager

from flask import Blueprint

chat = Blueprint('chat', __name__)
from . import events, views, models

# from api import client_count
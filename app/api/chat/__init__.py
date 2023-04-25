from flask import Blueprint

chat = Blueprint('chat', __name__)
from . import views, models, event

# from api import client_count
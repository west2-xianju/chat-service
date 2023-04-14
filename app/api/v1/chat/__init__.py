from flask import Blueprint

from .... import models

api = Blueprint("api", __name__)

from . import views


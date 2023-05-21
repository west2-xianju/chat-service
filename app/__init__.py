from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS

from config import config, Config
from .utils import ClientManager

socketio = SocketIO()
db = SQLAlchemy()
client_manager = ClientManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)

    # from .api.v1.chat import chat as chat_blueprint
    # app.register_blueprint(chat_blueprint)
    
    # from .api.chat import chat as chat_blueprint
    # app.register_blueprint(chat_blueprint, url_prefix='/chat')
    
    # from .api.notifications import notifications as notifications_blueprint
    # app.register_blueprint(notifications_blueprint, url_prefix='/notifications')
    
    # from .api.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/')

    socketio.init_app(app, cors_allowed_origins="*")
    
    return app

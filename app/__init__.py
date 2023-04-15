from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config, Config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)

    # from .api.v1.chat import chat as chat_blueprint
    # app.register_blueprint(chat_blueprint)
    
    from .chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint, url_prefix='/chat')
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app

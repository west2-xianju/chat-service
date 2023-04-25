# reimplement it by redis later on 

class ClientCounter():
    client_count = 0
    client_dict = {}

    def __init__(self):
        self.client_count = 0
        
    def is_online(self, user_id):
        return user_id in self.client_dict

    def add_user(self, user_id, sid):
        if user_id == None:
            raise ValueError('user_id cannot be None')
        
        if sid == None:
            raise ValueError('room_id cannot be None')
        
        # if user_id in self.client_dict and room_id in self.client_dict[user_id]:
        #     # user have already into this room
        #     return False
        
        if user_id in self.client_dict:
            self.client_dict[user_id].append(sid)
            return
        
        self.client_dict[user_id] = []
        self.client_dict[user_id].append(sid)
        self.client_count += 1
        
        return
    
    def remove_user(self, user_id, sid):
        if user_id == None:
            raise ValueError('user_id cannot be None')
        
        if  sid == None:
            raise ValueError('room_id cannot be None')
        
        if user_id not in self.client_dict:
            return
        
        self.client_dict[user_id].remove(sid)
        
        if len(self.client_dict[user_id]) == 0:
            self.client_dict.pop(user_id)
            self.client_count -= 1
            
        
        return
    
    def log_out(self, user_id):
        if user_id == None:
            raise ValueError('user_id cannot be None')
        
        if user_id not in self.client_dict:
            return
        
        self.client_dict.pop(user_id)
        self.client_count -= 1
        
        return
    

    def get(self):
        return self.client_count

    def set(self, count):
        self.client_count = count

    def __str__(self):
        return str(self.client_count)

    def __repr__(self):
        return str(self.client_count)

    def __int__(self):
        return self.client_count


client_counter = ClientCounter()


from flask import Blueprint

api = Blueprint('api', __name__)

from .auth import auth as auth_blueprint
api.register_blueprint(auth_blueprint, url_prefix='/auth')

from .chat import chat as chat_blueprint
api.register_blueprint(chat_blueprint, url_prefix='/chat')

from .notifications import notifications as notification_blueprint
api.register_blueprint(notification_blueprint, url_prefix='/notifications')

from .dev import dev as dev_blueprint
api.register_blueprint(dev_blueprint, url_prefix='/dev')
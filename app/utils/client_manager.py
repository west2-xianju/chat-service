import flask_socketio
class ClientManager():
    '''
    A class to manage client's connection.

    Attributes:
        USER_TABLE: A dict to store user's jwt token. kw-relation: user_id: jwt_token
        SID_TABLE: A dict to store user's sid. kw-relation: user_id: [array of sid]
        ROOM_TABLE: A dict to store user's room. kw-relation: sid: room_id
    '''

    USER_TABLE = {}
    SID_TABLE = {}
    ROOM_TABLE = {}

    def connect(self, user_id: int, jwt_token: str, init_sid: str):
        ''' Register a user's connection.
        :param user_id: user's id
        :param jwt_token: user's jwt token
        :param init_sid: user's initial sid(designed to be notification connection id)
        '''
        self.USER_TABLE[user_id] = jwt_token
        self.SID_TABLE[user_id] = [init_sid]

    def disconnect(self, user_id: int):
        ''' Unregister a user's connection.
        :param user_id: user's id
        '''
        if self.USER_TABLE.get(user_id, None) == None:
            raise ValueError('user not exist')

        
        for _ in self.SID_TABLE[user_id]:
            flask_socketio.disconnect(sid=_, namespace='/notification')
        
        self.USER_TABLE.pop(user_id)
        self.SID_TABLE.pop(user_id)

    def add_sid(self, user_id: int, sid: str):
        ''' Add a sid to a user's connection.
        :param user_id: user's id
        :param sid: user's sid'''
        if self.USER_TABLE.get(user_id, None) == None:
            raise ValueError('user not exist')

        self.SID_TABLE[user_id].append(sid)
        
    def add_room(self, sid, room):
        ''' Add a room to a user's connection.
        :param room: room's id
        :param sid: user's sid'''
        self.ROOM_TABLE[sid] = room

    def delete_room(self, sid):
        ''' Delete a room from a user's connection.
        :param sid: user's sid'''
        try:
            self.ROOM_TABLE.pop(sid)
        except:
            raise ValueError('sid not exist')

    def delete_sid_by_user_id(self, user_id: int, sid: str):
        ''' Delete a sid from a user's connection by appointed user_id.
        :param user_id: user's id
        :param sid: user's sid
        '''
        if self.USER_TABLE.get(user_id, None) == None:
            raise ValueError('user not exist')

        try:
            self.SID_TABLE[user_id].remove(sid)
        except ValueError:
            raise ValueError('sid not exist')
        
        # if no sid left, delete corresponding user_id
        if len(self.SID_TABLE[user_id]) == 0:
            self.USER_TABLE.pop(user_id)

    def delete_sid(self, sid):
        ''' Delete a sid from a user's connection.
        :param sid: user's sid
        '''
        for i in self.SID_TABLE:
            try:
                self.SID_TABLE[i].remove(sid)
            except ValueError:
                pass

        raise ValueError('sid not exist')

    def get_sid(self, user_id):
        ''' Get a user's sid.
        :param user_id: user's id'''
        if self.USER_TABLE.get(user_id, None) == None:
            raise ValueError('user not exist')

        return self.SID_TABLE[user_id]
    
    def get_user_id_by_sid(self, sid):
        ''' Get user_id by sid
        :param sid: user's sid'''
        for _ in self.SID_TABLE:
            if sid in self.SID_TABLE[_]:
                return _
        raise ValueError('sid not exist')
    
    def get_room_by_sid(self, sid):
        ''' Get room by sid
        :param sid: user's sid'''
        if sid not in self.ROOM_TABLE:
            print(self.ROOM_TABLE)
            raise ValueError('sid not exist')
        return self.ROOM_TABLE[sid]
    

    def get_user_count(self):
        ''' Get user count '''
        return len(self.USER_TABLE)

    def get_user_token(self, user_id):
        ''' Get user's jwt token
        :param user_id: user's id
        '''
        if self.USER_TABLE.get(user_id, None) == None:
            raise ValueError('user not exist')

        return self.USER_TABLE[user_id]

    def check_user_if_online(self, user_id):
        ''' Check if user is online
        :param user_id: user's id
        '''
        return user_id in self.USER_TABLE

    def show_user_table(self):
        ''' Show user table
        function: print user table
        '''
        for i in self.USER_TABLE:
            print(i, self.USER_TABLE[i])

    def show_sid_table(self):
        ''' Show sid table
        function: print sid table'''
        for i in self.SID_TABLE:
            print(i, self.SID_TABLE[i])


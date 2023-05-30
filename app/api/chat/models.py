from app import db
from datetime import datetime
# import enum
from sqlalchemy import *
from sqlalchemy.orm import synonym


class BaseModel:
    """Base for all models, providing save, delete and from_dict methods."""

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        """Deletes this model from the db (through db.session)"""
        db.session.delete(self)
        self.__commit()

    def save(self):
        """Adds this model to the db (through db.session)"""
        db.session.add(self)
        self.__commit()
        return self

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict).save()
    
# class testEnum(enum):
    

class Message(db.Model, BaseModel):
    __tablename__ = 'message'
    
    MESSAGE_TYPE_ENUM = ['plaintext', 'photo', 'voice', 'video', 'file']
    id = Column(Integer, nullable=True, primary_key=True, unique=True)
    room_id = Column(Integer, nullable=False)
    sender_id = Column(Integer, nullable=False)
    send_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    _detail = Column('detail' ,String(1024), default='')
    type = Column(Enum(*MESSAGE_TYPE_ENUM), nullable=False, default=MESSAGE_TYPE_ENUM[0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def detail(self):
        return self._detail

    @detail.setter
    def detail(self, detail):
        if detail == 'ill':
            self._detail = 'invalid'
            return
        # todo
        # check if context is valid
        self._detail = detail
        
    detail = synonym("_detail", descriptor=detail)
        
    def to_dict(self):
        return {
            # 'id': self.id,
            # 'room_id': self.room_id,
            'sender_id': self.sender_id,
            'send_time': datetime.isoformat(self.send_time, sep=' '),
            'detail': self._detail,
            'type': self.type, 
            }
    def to_dict_all(self):
        return {
            # 'id': self.id,
            'room_id': self.room_id,
            'sender_id': self.sender_id,
            'send_time': datetime.isoformat(self.send_time, sep=' '),
            'detail': self._detail,
            'type': self.type, 
            }

class Room(db.Model, BaseModel):
    __tablename__ = 'room'
    
    ROOM_STATE_ENUM = ['pending', 'ongoing', 'finished']
    room_id = Column(BigInteger, primary_key=True, unique=True)
    goods_id = Column(Integer)
    seller_id = Column(Integer, nullable=False)
    buyer_id = Column(Integer)
    state = Column(Enum(*ROOM_STATE_ENUM), nullable=False, default=ROOM_STATE_ENUM[0])
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'room_id': self.room_id,
            'goods_id': self.goods_id,
            'seller_id': self.seller_id,
            'buyer_id': self.buyer_id,
            'state': self.state,
            'create_time': datetime.isoformat(self.create_time, sep=' '),
        }
        
        
class Good(db.Model, BaseModel):
    __bind_key__ = 'app'
    __tablename__ = 'good'
    
    # GOOD_STATES_ENUM = ['pending', 'released', 'locked', 'sold', 'reported', 'canceled', 'deleted']
    GOOD_STATES_ENUM = ['pending', 'released', 'locked', 'sold', 'canceled', 'deleted']
    good_id = Column('uid', Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)
    state = Column(Enum(*GOOD_STATES_ENUM), nullable=False, default=GOOD_STATES_ENUM[0])
    game = Column(String(256))
    title = Column(String(256))
    detail = Column(String(256))
    price = Column(DECIMAL(10, 2))
    publish_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'uid': self.good_id,
            'seller_id': self.seller_id,
            'state': self.state,
            'game': self.game,
            'title': self.title,
            'detail': self.detail,
            'price': self.price,
            'publish_time': datetime.isoformat(self.publish_time, sep=' '),
            }
        

class User(db.Model, BaseModel):
    __bind_key__ = 'app'
    __tablename__ = 'user'
    
    user_id = Column('uid', Integer, primary_key=True)
    _username = Column("username", db.String(64), unique=True)
    _email = Column("email", db.String(64), unique=True)
    _password = Column('password', String(256))
    nickname = Column(String(40))
    realname = Column(String(40))
    id_number = Column(String(20))
    register_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    blocked = Column(Boolean, nullable=False, default=False)
    profile = ''
    
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        is_valid_length = check_length(username, 64)
        if not is_valid_length or not bool(USERNAME_REGEX.match(username)):
            raise ValueError(f"{username} is not a valid username")
        self._username = username

    username = synonym("_username", descriptor=username)
    
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not check_length(email, 64) or not bool(EMAIL_REGEX.match(email)):
            raise ValueError(f"{email} is not a valid email address")
        self._email = email

    email = synonym("_email", descriptor=email)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        if not bool(password):
            raise ValueError("no password given")

        hashed_password = hash_and_salt_password(password)
        if not check_length(hashed_password, 128):
            raise ValueError("not a valid password, hash is too long")
        self._password = hashed_password

    password = synonym("_password", descriptor=password)
    
    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'uid': self.user_id,
            'username': self.username,
            'nickname': self.nickname,
            'realname': self.realname,
            'id_number': self.id_number,
            'profile': '',
            'email': self.email,
            'blocked': self.blocked,
            'register_time': datetime.isoformat(self.register_time, sep=' ')
            }
        


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
    

MESSAGE_TYPE_ENUM = ['plaintext', 'photo', 'voice', 'video', 'file']
class Message(db.Model, BaseModel):
    __tablename__ = 'message'
    
    # id = db.Column(db.Integer, primary_key=True)
    # _username = db.Column("username", db.String(64), unique=True)
    # _email = db.Column("email", db.String(64), unique=True)
    # password_hash = db.Column(db.String(128))
    # member_since = db.Column(db.DateTime, default=datetime.utcnow)
    # last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # is_admin = db.Column(db.Boolean, default=False)
    # id = db.Column(db.integ, primary_key=True)
    id = Column(Integer, nullable=True, primary_key=True, unique=True)
    room_id = Column(Integer, nullable=False)
    sender_id = Column(Integer, nullable=False)
    send_time = Column(DateTime, nullable=False, default=datetime.utcnow())
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
            'send_time': self.send_time,
            'detail': self._detail,
            'type': self.type, 
            }
    def to_dict_all(self):
        return {
            # 'id': self.id,
            'room_id': self.room_id,
            'sender_id': self.sender_id,
            'send_time': self.send_time,
            'detail': self._detail,
            'type': self.type, 
            }

ROOM_STATE_ENUM = ['pending', 'ongoing', 'finished']
class Room(db.Model, BaseModel):
    __tablename__ = 'room'
    
    room_id = Column(Integer, primary_key=True, unique=True)
    goods_id = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=False)
    buyer_id = Column(Integer, nullable=False)
    state = Column(Enum(*ROOM_STATE_ENUM), nullable=False, default=ROOM_STATE_ENUM[0])
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'room_id': self.room_id,
            'goods_id': self.goods_id,
            'seller_id': self.seller_id,
            'buyer_id': self.buyer_id,
            'state': self.state,
            'create_time': self.create_time, 
        }
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
    

class Notification(db.Model, BaseModel):
    __tablename__ = 'notification'
    
    DEFAULT_NOTIFICATION_TITLE = 'New Notification'
    DEFAULT_NOTIFICATION_CONTENT = 'You have a new notification'
    NOTIFICATION_LEVEL_ENUM = ['normal', 'high', 'low', 'urgent']
    
    notification_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(1024), default=DEFAULT_NOTIFICATION_TITLE)
    content = Column(String(1024), default=DEFAULT_NOTIFICATION_CONTENT)
    level = Column(Enum(*NOTIFICATION_LEVEL_ENUM), nullable=False, default=NOTIFICATION_LEVEL_ENUM[0])
    send_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        
    def to_dict(self):
        return {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'level': self.level,
            'send_time': self.send_time
            }

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
    
class BlackList(db.Model, BaseModel):
    __tablename__ = 'blacklist'
    
    user_id = Column(Integer, primary_key=True, unique=True)
    blocked_user_id = Column(Integer, nullable=False)
    blocked_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'blocked_user_id': self.blocked_user_id,
        }
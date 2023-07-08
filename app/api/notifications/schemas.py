from pydantic import BaseModel
from typing import Optional
    # notification_id = Column(Integer, primary_key=True, unique=True)
    # user_id = Column(Integer, nullable=False)
    # title = Column(String(1024), default=DEFAULT_NOTIFICATION_TITLE)
    # content = Column(String(1024), default=DEFAULT_NOTIFICATION_CONTENT)
    # level = Column(Enum(*NOTIFICATION_LEVEL_ENUM), nullable=False, default=NOTIFICATION_LEVEL_ENUM[0])
    # send_time = Column(DateTime, nullable=False, default=datetime.utcnow)

class NotificationBase(BaseModel):
    title: str
    content: Optional[str]
    level: str
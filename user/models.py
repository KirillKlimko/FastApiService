from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from config import settings
from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, unique=True, primary_key=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=None)

    user = relationship('MeetingUsers', backref='user')

    def verify_password(self, password):
        return settings.pwd_context.verify(password, self.password)

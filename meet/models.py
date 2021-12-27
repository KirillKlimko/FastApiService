from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class MeetingUsers(Base):
    __tablename__ = 'meeting_users'

    id = Column(Integer, primary_key=True)
    meet_id = Column(Integer(), ForeignKey("meet.id"))
    user_id = Column(Integer(), ForeignKey("user.id"))


class Meet(Base):
    __tablename__ = 'meet'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=None)
    meeting_time = Column(DateTime, default=None)
    users = relationship('MeetingUsers', backref='meet')

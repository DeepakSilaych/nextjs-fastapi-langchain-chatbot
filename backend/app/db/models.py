from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    message = Column(Text)
    is_user = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
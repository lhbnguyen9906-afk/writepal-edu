from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class PreSurvey(Base):
    __tablename__ = "presurveys"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    level = Column(String)
    goal = Column(String)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    title = Column(String, default="New Chat")

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)
    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from datetime import datetime

from .db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())

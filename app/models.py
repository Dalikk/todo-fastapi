from sqlalchemy import Column, Boolean, Integer, String, DateTime
from datetime import datetime

from .database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())

from pydantic import BaseModel
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    description: str | None = None
    done: bool = False


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

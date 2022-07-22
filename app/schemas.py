from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool

    class Config:
        orm_mode = True


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

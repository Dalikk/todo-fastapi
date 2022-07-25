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
    user_id: int

    class Config:
        orm_mode = True


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


class UserWithTodos(User):
    todos: list[Todo] = []


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

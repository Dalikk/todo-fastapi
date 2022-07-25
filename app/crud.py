from sqlalchemy.orm import Session

from . import models, schemas
from .utils.auth import get_password_hash


def get_users(db: Session, skip: int, limit: int):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


def get_user(db: Session, username: str):
    return db.query(models.User).filter_by(username=username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pass = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_pass,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter_by(id=todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def get_user_todos(db: Session, user: models.User):
    user_todos = user.todos.all()


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

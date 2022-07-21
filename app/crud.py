from sqlalchemy.orm import Session

from . import models, schemas


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter_by(id=todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

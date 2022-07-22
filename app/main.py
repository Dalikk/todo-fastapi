from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from . import schemas, models, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return RedirectResponse('/docs')


@app.get('/todos/', response_model=list[schemas.Todo])
async def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_todos = crud.get_todos(db, skip, limit)
    return db_todos


@app.get('/todos/{todo_id}', response_model=schemas.Todo)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail="Not found",
        )
    return db_todo


@app.post('/todos/', response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from . import schemas, models, crud
from .database import SessionLocal
from .dependencies import get_db
from .utils.auth import authenticate_user, create_access_token, get_current_active_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


@app.get('/')
async def root():
    return RedirectResponse('/docs')


@app.post('/token', response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/users/', response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


@app.get('/users/me', response_model=schemas.User)
async def read_user_me(current_user: schemas.User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get('/users/{username}', response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_db = crud.create_user(db=db, user=user)
    return user_db


# @app.get('/user/todos')
# def read_user_todos(current_user: Depends(get_current_active_user)):
#     pass


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
async def create_todo(
        todo: schemas.TodoCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_active_user)
):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)


@app.get('/secret-route/')
def get_secret_route(current_user=Depends(get_current_active_user)):
    return {"message": "you are in private route"}


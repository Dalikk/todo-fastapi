from fastapi import FastAPI
from . import schemas
app = FastAPI()

todos = [
    {
        "id": 1,
        "title": "first todo",
        "created_at": "2022-07-21 07:15:54.916539",
        "done": False
    },
    {
        "id": 2,
        "title": "second todo",
        "description": "some description...",
        "created_at": "2022-07-21 07:15:54.916539",
        "done": False
    },
]


@app.get('/todos/', response_model=list[schemas.Todo])
async def main(skip: int = 0, limit: int = 10):
    return todos[skip:limit]

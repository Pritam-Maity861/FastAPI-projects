from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from typing import Annotated
from fastapi import Depends
from app.services.todo import TodoService

from app.repositories.todo import TodoRepository


def get_todo_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = TodoRepository(db)
    return TodoService(repo)


Todo_service_depandency = Annotated[AsyncSession, Depends(get_todo_service)]

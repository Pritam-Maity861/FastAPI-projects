from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo import TodoService


todoRouter = APIRouter(prefix="/todos", tags=["Todo"])

def get_todo_service(db:Annotated[AsyncSession,Depends(get_db)]):
    repo=TodoRepository(db)
    return TodoService(repo)

Todo_service_depandency=Annotated[AsyncSession,Depends(get_todo_service)]

@todoRouter.get("/",response_model=list[TodoResponse])
async def get_all_todos(service:Todo_service_depandency):
    return await service.get_all()


@todoRouter.post("/",response_model=TodoResponse,status_code=status.HTTP_201_CREATED)
async def create_todo(todo_in:TodoCreate,service:Todo_service_depandency):
    return await service.create(todo_in)


@todoRouter.get("/{todo_id}",response_model=TodoResponse)
async def get_todo_by_id(todo_id:UUID,service:Todo_service_depandency):
     todo=await service.get_by_id(todo_id)
     if todo is None:
         return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo not found")
     return todo


@todoRouter.patch("/{todo_id}",response_model=TodoResponse)
async def update_todo_by_id(todo_id:UUID,todo_in:TodoUpdate,service:Todo_service_depandency):
     todo=await service.update(todo_id,todo_in)
     if todo is None:
         return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo not found")
     return todo


@todoRouter.delete("/{todo_id}", response_model=TodoResponse)
async def delete_todo(todo_id: UUID,service: Todo_service_depandency):
    todo = await service.delete_todo(todo_id)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo not found")

    return todo
     


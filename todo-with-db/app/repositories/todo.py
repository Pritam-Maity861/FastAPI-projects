from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo


class TodoRepository:
    def __init__(self,db:AsyncSession):
        self.db=db

    async def create(self,todo:Todo)->Todo:
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)

        return todo
    

    async def get_all(self)->list[Todo]:
        result=await self.db.execute(select(Todo).order_by(Todo.id))
        return list(result.scalars().all())
    

    async def get_by_id(self,todo_id:UUID)->Todo|None:
        return await self.db.get(Todo,todo_id)
    

    async def delete(self, todo: Todo) -> Todo:
            await self.db.delete(todo)
            await self.db.commit()

            return todo


    async def update_todo(self,todo:Todo,updated_data:dict[str,Any])->Todo:
        for field, value in updated_data.items():
            setattr(todo, field, value)

        await self.db.commit()
        await self.db.refresh(todo)

        return todo

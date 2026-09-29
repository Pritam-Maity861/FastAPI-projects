from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.schemas.todo import TodoListParams


class TodoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, todo: Todo) -> Todo:
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)

        return todo

    async def get_all(
        self, user_id: UUID, filters: TodoListParams
    ) -> tuple[list[Todo], int]:
        conditions = [Todo.user_id == user_id]

        if filters.is_completed is not None:
            conditions.append(Todo.is_completed == filters.is_completed)

        count_query = select(func.count(Todo.id)).select_from(Todo).where(*conditions)
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()

        sort_columns = {"created_at": Todo.created_at, "title": Todo.title}
        sort_column = sort_columns[filters.sort_by]

        order_by = (
            sort_column.asc() if filters.sort_order == "asc" else sort_column.desc()
        )

        offset = (filters.page - 1) * filters.limit
        limit = filters.limit

        todos_query = (
            select(Todo)
            .where(*conditions)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(todos_query)
        return list(result.scalars().all()), total

    async def get_by_id(self, todo_id: UUID) -> Todo | None:
        return await self.db.get(Todo, todo_id)

    async def delete(self, todo: Todo) -> Todo:
        await self.db.delete(todo)
        await self.db.commit()

        return todo

    async def update_todo(self, todo: Todo, updated_data: dict[str, Any]) -> Todo:
        for field, value in updated_data.items():
            setattr(todo, field, value)

        await self.db.commit()
        await self.db.refresh(todo)

        return todo

    async def get_user_todos_for_export(
        self, user_id, is_completed: bool | None = None
    ) -> list[Todo]:
        query = select(Todo).where(Todo.user_id == user_id)
        if is_completed is not None:
            query = query.where(Todo.is_completed == is_completed)

        query = query.order_by(Todo.created_at.desc())

        result = await self.db.execute(query)

        return list(result.scalars().all())

from uuid import UUID

from app.errors.exceptions import DuplicateTodoError
from app.models.todo import Todo
from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo

    async def create(self, todo_in: TodoCreate) -> Todo:
        try:
            return await self.repo.create(Todo(**todo_in.model_dump()))
        except:  # noqa: E722
            raise DuplicateTodoError()

    async def get_all(self) -> list[Todo]:
        return await self.repo.get_all()

    async def get_by_id(self, todo_id: UUID) -> Todo | None:
        todo = await self.repo.get_by_id(todo_id)

        if todo is None:
            return None
        return todo

    async def update(self, todo_id: UUID, todo_in: TodoUpdate) -> Todo | None:
        todo = await self.repo.get_by_id(todo_id)

        if todo is None:
            return None

        updated_data = todo_in.model_dump(exclude_unset=True)
        if not updated_data:
            return todo
        try:
            return await self.repo.update_todo(todo, updated_data)
        except:  # noqa: E722
            raise DuplicateTodoError()

    async def delete_todo(self, todo_id: UUID) -> Todo | None:
        todo = await self.repo.get_by_id(todo_id)

        if todo is None:
            return None
        return await self.repo.delete(todo)

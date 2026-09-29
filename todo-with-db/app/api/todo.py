from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies.todo import Todo_service_depandency
from app.errors.exceptions import TodoNotFoundError
from app.schemas.common_response_schema import SuccessResponse
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.utils.response import success_response

todoRouter = APIRouter(prefix="/todos", tags=["Todo"])


@todoRouter.get("/", response_model=SuccessResponse[list[TodoResponse]])
async def get_all_todos(service: Todo_service_depandency):
    todos = await service.get_all()
    return success_response(data=todos, message="All todo fetched successfully")


@todoRouter.post(
    "/",
    response_model=SuccessResponse[TodoResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(todo_in: TodoCreate, service: Todo_service_depandency):
    todo = await service.create(todo_in)
    return success_response(data=todo, message="Todo created successfully")


@todoRouter.get("/{todo_id}", response_model=SuccessResponse[TodoResponse])
async def get_todo_by_id(todo_id: UUID, service: Todo_service_depandency):
    todo = await service.get_by_id(todo_id)
    if todo is None:
        raise TodoNotFoundError()
    return success_response(data=todo, message="todo fetched successfully")


@todoRouter.patch("/{todo_id}", response_model=SuccessResponse[TodoResponse])
async def update_todo_by_id(
    todo_id: UUID, todo_in: TodoUpdate, service: Todo_service_depandency
):
    todo = await service.update(todo_id, todo_in)
    if todo is None:
        raise TodoNotFoundError()
    return success_response(data=todo, message="Todo updated Successfully")


@todoRouter.delete("/{todo_id}", response_model=SuccessResponse[TodoResponse])
async def delete_todo(todo_id: UUID, service: Todo_service_depandency):
    todo = await service.delete_todo(todo_id)

    if todo is None:
        raise TodoNotFoundError()

    return success_response(data=todo, message="todo deleted successfully")

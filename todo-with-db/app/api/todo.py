from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Query, status
from fastapi.responses import StreamingResponse

from app.dependencies.security import CurrentUser
from app.dependencies.todo import Todo_service_depandency
from app.errors.exceptions import TodoNotFoundError
from app.schemas.common_response_schema import SuccessResponse
from app.schemas.todo import TodoCreate, TodoListParams, TodoResponse, TodoUpdate
from app.services.mail_service import send_todo_export_mail
from app.utils.response import success_response
from app.utils.todo_export import todos_to_json

todoRouter = APIRouter(prefix="/todos", tags=["Todo"])


@todoRouter.get("/", response_model=SuccessResponse[list[TodoResponse]])
async def get_all_todos(
    service: Todo_service_depandency,
    curr_user: CurrentUser,
    filters: Annotated[TodoListParams, Query()],
):
    user_id = curr_user.id
    todos, total = await service.get_all(user_id, filters)
    total_pages = (total + filters.limit - 1) // filters.limit
    return success_response(
        data=todos,
        message="All todo fetched successfully",
        meta={
            "page": filters.page,
            "limit": filters.limit,
            "total_items": total,
            "total_pages": total_pages,
            "has_next": filters.page < total_pages,
            "has_previous": filters.page > 1,
        },
    )


@todoRouter.post(
    "/",
    response_model=SuccessResponse[TodoResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    todo_in: TodoCreate, service: Todo_service_depandency, curr_user: CurrentUser
):
    user_id = curr_user.id
    todo = await service.create(todo_in, user_id)
    return success_response(data=todo, message="Todo created successfully")


@todoRouter.get("/export-todos")
async def export_all_your_todo(
    service: Todo_service_depandency,
    background_tasks: BackgroundTasks,
    curr_user: CurrentUser,
    is_completed: bool | None = None,
):
    todos = await service.get_user_todos_for_export(
        user_id=curr_user.id,
        is_completed=is_completed,
    )

    file = todos_to_json(todos)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # noqa: DTZ005

    filename = f"{curr_user.full_name}_{timestamp}.json"

    filedata = file.getvalue()

    background_tasks.add_task(
        send_todo_export_mail,
        recipient=curr_user.email,
        file_data=filedata,
        filename=filename,
    )

    return success_response(
        data={
            "filename": filename,
            "message": "Todo export has been sent to your email.",
        },
        message="Todo export generated successfully",
    )


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

import io
import json

from app.models.todo import Todo


def todos_to_json(todos: list[Todo]) -> io.BytesIO:
    data = [
        {
            "id": str(todo.id),
            "title": todo.title,
            "description": todo.description,
            "is_completed": todo.is_completed,
            "created_at": (
                todo.created_at.isoformat()
                if todo.created_at
                else None
            ),
            "updated_at": (
                todo.updated_at.isoformat()
                if todo.updated_at
                else None
            ),
        }
        for todo in todos
    ]

    json_data = json.dumps(
        data,
        indent=4,
        ensure_ascii=False,
    )

    file = io.BytesIO(
        json_data.encode("utf-8")
    )

    file.seek(0)

    return file

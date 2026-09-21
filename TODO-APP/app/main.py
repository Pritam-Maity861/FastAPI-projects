from fastapi import FastAPI, HTTPException, Query, status
from datetime import datetime
from typing import Optional
from .todo_schema import CategoryIn,CategoryOut,CategoryUpdate,TodoIn,TodoOut,UpdateTodo

app = FastAPI(title="TODO-APP")


@app.get("/health")
async def check_health():
    return {"message": "OK"}


"""
In memory data storage
"""
categories = {}
todos = {}

category_id_counter = 1
todo_id_counter = 1


"""
CRUD for categories
"""


# create category
@app.post(
    "/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED
)
async def create_category(category_data: CategoryIn):
    global category_id_counter
    for category in categories.values():
        if category["name"].lower() == category_data.name.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="category is already exist.",
            )

    new_category = {"id": category_id_counter, "name": category_data.name}

    categories[category_id_counter] = new_category
    category_id_counter += 1

    return new_category


# get all category
@app.get("/categories", response_model=list[CategoryOut])
async def get_categories():
    return list(categories.values())


# update Category
@app.patch(
    "/categories/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
)
async def update_category(category_id: int, category_data: CategoryUpdate):
    if category_id not in categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="category id not exist."
        )
    for cat_id, category_name in categories.items():
        if (
            cat_id != category_id
            and category_name["name"].lower() == category_data.name.lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="category with this name already exist.",
            )
    categories[category_id]["name"] = category_data.name

    return categories[category_id]


# delete category
@app.delete("/category/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int):
    if category_id not in categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="category id not exist."
        )

    # get all the todos having this category so that while deleting the category its auto delete all the todos having that category
    todo_ids = [
        todo_id for todo_id, todo in todos.items() if todo["category_id"] == category_id
    ]

    print(todo_ids)

    for todo_id in todo_ids:
        del todos[todo_id]

    del categories[category_id]

    return {
        "message": "Category deleted successfully",
        "deleted_todos_count": len(todo_ids),
    }


"""
CRUD for Todos
"""


# create todo
@app.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_data: TodoIn):
    global todo_id_counter
    if todo_data.category_id not in categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found, enter a valid category.",
        )

    for todo in todos.values():
        if todo["title"].lower() == todo_data.title.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Same todo title is already exist.",
            )

    new_todo = {
        "id": todo_id_counter,
        "title": todo_data.title,
        "description": todo_data.description,
        "is_completed": todo_data.is_completed,
        "priority": todo_data.priority,
        "category_id": todo_data.category_id,
        "status": todo_data.status,
        "created_at": datetime.now(),
    }

    todos[todo_id_counter] = new_todo
    todo_id_counter += 1

    return new_todo


# get all todos
@app.get("/todos", response_model=list[TodoOut])
def get_todos(
    completed: Optional[bool] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    todo_list = list(todos.values())
    if completed is not None:
        todo_list = [todo for todo in todo_list if todo["is_completed"] == completed]

    if search:
        search_text = search.lower()

        todo_list = [
            todo
            for todo in todo_list
            if (
                search_text in todo["title"].lower()
                or (
                    todo["description"] is not None
                    and search_text in todo["description"].lower()
                )
            )
        ]

    start = (page - 1) * limit
    end = start + limit

    return todo_list[start:end]


# get todo by todo_id
@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return todos[todo_id]


# get todo by category
@app.get("/categories/{category_id}/todos", response_model=list[TodoOut])
def get_todos_by_category(category_id: int):
    if category_id not in categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    category_todos = [
        todo for todo in todos.values() if todo["category_id"] == category_id
    ]

    return category_todos


# update todo by todo_id
@app.patch("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, todo_data: UpdateTodo):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    if todo_data.category_id is not None:
        if todo_data.category_id not in categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

    update_data = todo_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        todos[todo_id][field] = value

    return todos[todo_id]


# delete todo by todo_id
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    del todos[todo_id]
    return {"message": "Todo deleted successfully"}


# delete todo by category
@app.delete("/categories/{category_id}/todos")
def delete_todos_by_category(category_id: int):
    if category_id not in categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    todo_ids = [
        todo_id for todo_id, todo in todos.items() if todo["category_id"] == category_id
    ]

    for todo_id in todo_ids:
        del todos[todo_id]
    return {"message": "Todos deleted successfully", "deleted_count": len(todo_ids)}

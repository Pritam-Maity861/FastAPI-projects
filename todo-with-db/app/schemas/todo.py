from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime
from uuid import UUID


class TodoBase(BaseModel):
    title:str=Field(...,min_length=3,max_length=255 )
    description:str|None=None
    is_completed:bool=False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = None
    is_completed: bool | None = None


class TodoResponse(TodoBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
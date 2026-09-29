from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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
    user_id:UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TodoListParams(BaseModel):
    is_completed:bool|None=None
    sort_by:Literal["created_at","title"]="created_at"
    sort_order:Literal["asc","desc"]="asc"

    limit:int =Field(ge=1,le=100,default=10)
    page:int=Field(ge=1,default=1)
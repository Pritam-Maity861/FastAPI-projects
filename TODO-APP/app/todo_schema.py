from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

'''
category schema
'''
class CategoryBase(BaseModel):
    name:str


class CategoryIn(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id:int

    model_config=ConfigDict(from_attributes=True)


'''
Todo schema
'''
class TodoBase(BaseModel):
    title:str
    description:Optional[str]=None
    is_completed:bool=False
    priority:int=1
    category_id:int
    status:str="pending"


class TodoIn(TodoBase):
    pass


class UpdateTodo(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None
    is_completed:Optional[bool]=None
    priority:Optional[int]=None
    category_id:int=None
    status:Optional[str]=None


class TodoOut(TodoBase):
    id:int
    created_at:datetime

    model_config=ConfigDict(from_attributes=True)




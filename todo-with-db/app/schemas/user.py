from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=12)


class UserLogin(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length=6, max_length=12)

class TokenResponse(BaseModel):
    access_token: str

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3, max_length=255)
    email: EmailStr | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool 
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

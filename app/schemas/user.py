from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email:EmailStr
    full_name: str

class UserCreate(UserBase):
    password:str

class UserPublic(UserBase):
    id:int
    is_active:bool
    is_verified:bool
    created_at:datetime

    class Config:
        from_attributes = True
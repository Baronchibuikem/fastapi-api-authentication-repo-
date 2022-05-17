from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    phone_number: str
    is_admin: bool

    class Config:
        """This will tell pydantic to read our value from sqlachemy"""
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

    class Config:
        """This will tell pydantic to read our value from sqlachemy"""
        orm_mode = True

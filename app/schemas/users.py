from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    DOCTOR = "doctor"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str]
    role: UserRole
    password: str
    unit_id: Optional[int]

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    role: Optional[UserRole]
    password: Optional[str]
    unit_id: Optional[int]

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    role: UserRole
    unit_id: Optional[int]
    is_active: bool

    class Config:
        orm_mode = True

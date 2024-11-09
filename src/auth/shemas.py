

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    number: str
    password: str
    is_active: Optional[bool] = True  


class UserAuthShema(BaseModel):
    email: EmailStr
    password: str  
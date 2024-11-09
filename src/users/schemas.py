from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    number: str
    hashed_password: str
    is_active: bool





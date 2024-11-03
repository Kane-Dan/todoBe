from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    number: str
    hashed_password: str
    is_active: bool

class UserCreateSchema(BaseModel):
    name: str
    email: str
    number: str
    password: str
    is_active: Optional[bool] = True  # Поле необязательно, по умолчанию True
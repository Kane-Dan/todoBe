from typing import Optional
from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    is_active: bool
    

class TaskCreateSchema(BaseModel):
    title: str
    description: str
    is_active: Optional[bool] = True  
    user_id: int

class TaskUpdate(BaseModel):
    title: str
    description: str
    is_active: Optional[bool] = True   
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from .models import User
from .schemas import UserCreateSchema
from passlib.context import CryptContext
from src.database import async_session_maker

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/{id}")
async def get_user(id: int):
    async with async_session_maker() as session:
        return await session.query(User).filter(User.id == id).first()

@router.post("/create")
async def create_user(data:UserCreateSchema):
    async with async_session_maker() as session:
        hashed_password = pwd_context.hash(data.password)
        new_user = User(
            name=data.name,
            email=data.email,
            number=data.number,
            hashed_password=hashed_password,
        )
        session.add(new_user)
        await session.commit()
    return JSONResponse(status_code=200, content={"detail": "User created successfully"})

@router.delete("/delete/{id}")
async def delete_post(id:int):
    async with async_session_maker() as session:
        await session.execute(delete(User).where(User.id == id))
        await session.commit()       
    return JSONResponse(status_code=200, content={"detail": "User deleted successfully"})
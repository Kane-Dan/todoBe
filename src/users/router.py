from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from .models import User

from passlib.context import CryptContext
from .services import UsersSercvices
from sqlalchemy.future import select

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/{id}")
async def get_user(id: int):
   return await UsersSercvices.get_user_by_id(id)

  

@router.delete("/delete/{id}")
async def delete_user(id:int):
    return await UsersSercvices.delete_user_by_id(id)

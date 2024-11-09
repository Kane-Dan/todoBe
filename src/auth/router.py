from fastapi import APIRouter
from src.auth.services import AuthServices
from src.auth.shemas import UserRegisterSchema,UserAuthShema
from src.users.services import UsersSercvices




router = APIRouter()

@router.post("/register")
async def register(data:UserRegisterSchema):
    return await UsersSercvices.create_user(data) 

@router.post("/auth")
async def login(data:UserAuthShema):
    return await AuthServices.auth(data)
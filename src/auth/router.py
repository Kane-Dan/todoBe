from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.auth.services import AuthServices
from src.auth.shemas import UserRegisterSchema, UserAuthShema

router = APIRouter()


@router.post("/register")
async def register(data: UserRegisterSchema):
    data = await AuthServices.register(data)
    return JSONResponse(status_code=200, content={"detail": data})


@router.post("/auth")
async def login(data: UserAuthShema):
    data = await AuthServices.login(data)
    return JSONResponse(status_code=200, content={"detail": data})

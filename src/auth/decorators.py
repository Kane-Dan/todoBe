from functools import wraps
from fastapi import HTTPException, Request, status
from src.auth.services import AuthServices

def require_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        print(request)
        if not request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request object is missing")

        # Извлечение токена из заголовка Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or invalid")

        token = auth_header.split(" ")[1]

        # Проверка токена
        await AuthServices.verify_token(token)
        
        return await func(*args, **kwargs)
    return wrapper

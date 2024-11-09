from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.database import async_session_maker
from src.users.services import UsersSercvices
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from src.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from src.auth.models import Token
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthServices:

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def login(data):
        async with async_session_maker() as session:
            user = await UsersSercvices.get_user_by_email(email=data.email)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден",
                )

            if not pwd_context.verify(data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
                )

            # Проверка на существование старого токена
            result = await session.execute(
                select(Token).where(Token.user_id == user.id)
            )
            existing_token = result.scalar_one_or_none()

            if existing_token:
                # Удаление старого токена
                await session.delete(existing_token)
                await session.commit()

            # Создание нового токена
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = AuthServices.create_access_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )

            # Сохранение нового токена в базе данных
            new_token = Token(token=access_token, user_id=user.id)
            session.add(new_token)
            await session.commit()

            return {"access_token": access_token, "token_type": "bearer"}

    async def register(data):
        # Хэшируем пароль
        hashed_password = pwd_context.hash(data.password)
        # Преобразуем объект Pydantic в словарь и заменяем пароль на хэшированный
        new_data = data.dict()
        new_data["hashed_password"] = hashed_password
        return await UsersSercvices.create_user(new_data)

    async def verify_token(token: str = Depends(oauth2_scheme)):
        """Функция для проверки токена"""
        try:
            # Декодирование токена для проверки срока действия
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")

            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Проверка наличия токена в базе данных
        async with async_session_maker() as session:
            result = await session.execute(select(Token).where(Token.token == token))
            token_entry = result.scalar_one_or_none()

            if not token_entry:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return token_entry.user_id  # Или возвращайте данные пользователя
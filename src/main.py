from fastapi import FastAPI
from src.users.router import router as users_router
from src.tasks.router import router as task_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(task_router, prefix= "/tasks")
app.include_router(users_router, prefix="/users")


origins = [
    "http://localhost",
    "http://localhost:8080",  # Разрешение запросов с React, Vue или другого локального фронтенд-сервера
    "http://127.0.0.1:8080",
    "http://192.168.68.105:8080", 
    "http://192.168.68.109:8080" # Если вы тестируете API с другого локального хоста
    # Добавляйте сюда любые другие источники
]

# Подключение CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,  # Разрешение отправки куки
    allow_methods=["*"],  # Разрешение всех методов: GET, POST, PUT, DELETE и т.д.
    allow_headers=["*"],  # Разрешение всех заголовков
)    
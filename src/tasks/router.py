from fastapi import APIRouter, HTTPException, Request 
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select,update

from src.auth.decorators import require_auth
from .schemas import TaskCreateSchema, TaskSchema, TaskUpdate
from src.database import async_session_maker
from src.tasks.models import Task

router = APIRouter()
# Создание поста
@router.post("/create")
@require_auth
async def create_post(request: Request, data:TaskCreateSchema):
    async with async_session_maker() as session:
        new_task= Task(
            title = data.title,
            description = data.description,
            user_id = data.user_id
        )
        session.add(new_task)
        await session.commit()
    return JSONResponse(status_code=200, content={"detail": "Task created successfully"})


# Удаление поста
@router.delete("/delete/{id}")
async def delete_post(id:int):
    async with async_session_maker() as session:
        await session.execute(delete(Task).where(Task.id == id))
        await session.commit()       
    return JSONResponse(status_code=200, content={"detail": "Task deleted successfully"})


# Вывод всех тасков
@router.get("/all")
async def get_all_tasks():
    async with async_session_maker() as session:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        return tasks
    
# Вывод таски по id
@router.get("/{id}")
async def get_all_tasks(id:int):
    async with async_session_maker() as session:
        result = await session.execute(select(Task).where(Task.id == id))
        task = result.scalars().all()
        return task[0]
    
# изменение таска
@router.put("/update/{id}")
async def update_post(id: int, data: TaskUpdate):
    async with async_session_maker() as session:
        async with session.begin(): 
            query = update(Task).where(Task.id == id).values(
                title=data.title,
                description=data.description
            )
            result = await session.execute(query)

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Task not found")

            await session.commit()

    return JSONResponse(status_code=200, content={"detail": "Task updated successfully"})
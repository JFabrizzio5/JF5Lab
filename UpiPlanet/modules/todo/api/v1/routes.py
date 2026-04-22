from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_sql_db
from modules.todo.models.models import Todo
from sqlalchemy import select

router = APIRouter()

@router.get("/")
async def list_todos(db: AsyncSession = Depends(get_sql_db)):
    result = await db.execute(select(Todo))
    return result.scalars().all()

@router.post("/")
async def create_todo(title: str, description: str = None, db: AsyncSession = Depends(get_sql_db)):
    todo = Todo(title=title, description=description)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

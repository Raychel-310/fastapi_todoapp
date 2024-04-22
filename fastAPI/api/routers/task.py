from typing import List

# from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task as task_crud
from api.db import get_db

import api.schemas.task as task_schema

from datetime import datetime, timedelta

router = APIRouter()

tasks = []

@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    tasks_from_db = await task_crud.get_tasks_with_done(db)
    tasks.extend(tasks_from_db)
    return tasks_from_db

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    created_task = await task_crud.create_task(db, task_body)
    tasks.append(created_task)
    return created_task

# @router.get("/tasks/before-deadline", response_model=List[task_schema.Task])
# async def get_tasks_before_deadline(date: datetime):
#     tasks_before_date = [task for task in tasks if task.deadline < date]
#     print(tasks)
#     print("Tasks before date:", tasks_before_date)
#     return tasks_before_date

@router.get("/tasks/before-deadline", response_model=List[task_schema.Task])
async def get_tasks_before_deadline(date: datetime, db: AsyncSession = Depends(get_db)):
    tasks = await task_crud.get_tasks_with_done(db)  # データベースからタスクを取得

    tasks_before_date = [task for task in tasks if task.deadline < date]
    print(tasks)
    print("Tasks before date:", tasks_before_date)
    return tasks_before_date

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)
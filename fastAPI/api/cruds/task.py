from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.engine import Result

from datetime import datetime

import api.models.task as task_model
import api.schemas.task as task_schema

async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Task.date,
                task_model.Task.deadline,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()

async def get_tasks_before_deadline(db: AsyncSession, deadline: datetime) -> List[task_model.Task]:
    result: Result = await db.execute(
            select(task_model.Task).filter(task_model.Task.deadline <= deadline)
    )
    tasks: List[task_model.Task] = result.all()
    return tasks

async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None # 要素が一つであってもtupleで返却されるので1つ目の要素を取り出す

async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    original.date = task_create.date
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()
from typing import Optional

from pydantic import BaseModel, Field

from datetime import datetime, timedelta

class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    deadline: Optional[datetime] = Field(None, example="2024-04-20T10:30:00")
    #date: Optional[datetime] = Field(None, example="2024-04-20T10:30:00")

class TaskCreate(TaskBase):
    pass
    # date: Optional[str] = Field(None, example="4月17日")

class TaskCreateResponse(TaskCreate):
    id: int
    # title: str
    # date: str

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    #date: str
    # title: Optional[str] = Field(None, example="クリーニングを取りに行く")
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True
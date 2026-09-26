from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID


class ReminderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=1000)
    remind_at: datetime
    recurrence: Literal["once", "daily", "weekly"] = "once"


class Reminder(ReminderCreate):
    id: UUID
    is_active: bool
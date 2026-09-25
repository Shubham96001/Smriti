"""
SmritiSaathi — Reminder Schemas
"""

from datetime import datetime, time
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class ReminderCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    reminder_type: str = Field(default="other", max_length=50)
    schedule_time: time
    recurrence: str = Field(default="daily", max_length=20)
    patient_profile_id: Optional[UUID] = None  # Required for caregiver creating for patient


class ReminderUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    reminder_type: Optional[str] = Field(None, max_length=50)
    schedule_time: Optional[time] = None
    recurrence: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None


class ReminderOut(BaseModel):
    id: UUID
    patient_profile_id: UUID
    created_by_user_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    reminder_type: str
    schedule_time: time
    recurrence: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ReminderEventCreate(BaseModel):
    status: str = Field(..., max_length=20)  # completed, postponed, missed
    notes: Optional[str] = None


class ReminderEventOut(BaseModel):
    id: UUID
    reminder_id: UUID
    status: str
    event_time: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class ReminderListResponse(BaseModel):
    reminders: List[ReminderOut] = []
    total: int = 0

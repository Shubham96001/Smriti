"""
SmritiSaathi — Patient Schemas
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PatientProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    preferred_language: str
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    baseline_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PatientProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    preferred_language: Optional[str] = Field(None, max_length=10)
    contact_phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=255)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)


class PatientDashboardResponse(BaseModel):
    """Data for the patient dashboard — fetched from DB, not hardcoded."""
    profile: PatientProfileResponse
    baseline_completed: bool
    total_games_played: int = 0
    total_memory_items: int = 0
    active_reminders: int = 0
    recent_accuracy: Optional[float] = None
    last_activity: Optional[datetime] = None

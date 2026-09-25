"""
SmritiSaathi — Caregiver Schemas
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class CaregiverProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    full_name: str
    contact_phone: Optional[str] = None
    relationship_type: Optional[str] = None
    invitation_code: str
    created_at: datetime

    class Config:
        from_attributes = True


class LinkedPatientSummary(BaseModel):
    """Summary of a patient linked to a caregiver — for the caregiver dashboard."""
    patient_profile_id: UUID
    full_name: str
    preferred_language: str
    baseline_completed: bool
    total_games_played: int = 0
    recent_accuracy: Optional[float] = None
    active_reminders: int = 0
    missed_reminders_week: int = 0
    last_activity: Optional[datetime] = None
    link_status: str


class LinkPatientRequest(BaseModel):
    """Request to link a patient to this caregiver using an invitation code or patient email."""
    patient_email: Optional[str] = None
    invitation_code: Optional[str] = None


class CaregiverDashboardResponse(BaseModel):
    """Caregiver dashboard data — all fetched from PostgreSQL."""
    profile: CaregiverProfileResponse
    linked_patients: List[LinkedPatientSummary] = []
    unread_alerts: int = 0
    total_alerts: int = 0

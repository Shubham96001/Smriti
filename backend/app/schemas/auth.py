"""
SmritiSaathi — Auth Schemas

Request/response models for registration, login, and token responses.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ── Registration ──

class PatientRegisterRequest(BaseModel):
    """Patient registration form fields."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    preferred_language: str = Field(default="en", max_length=10)
    contact_phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=255)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    consent_acknowledged: bool = False
    caregiver_invitation_code: Optional[str] = Field(None, max_length=12)


class CaregiverRegisterRequest(BaseModel):
    """Caregiver registration form fields."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=20)
    relationship_type: Optional[str] = Field(None, max_length=50)
    consent_acknowledged: bool = False


# ── Login ──

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── Token Response ──

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    role: str
    full_name: str
    baseline_completed: Optional[bool] = None


# ── User Info ──

class UserInfo(BaseModel):
    id: UUID
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

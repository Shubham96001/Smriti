from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)
    role: Literal["patient", "caregiver", "hcw"] = "patient"
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    preferred_language: str = Field(default="en", max_length=10)
    contact_phone: str | None = Field(default=None, max_length=30)
    address: str | None = None
    relationship_type: str | None = Field(default=None, max_length=50)
    consent_acknowledged: bool = False


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    full_name: str
    is_active: bool
    baseline_completed: bool | None = None
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
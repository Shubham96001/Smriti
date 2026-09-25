"""
SmritiSaathi — Assessment Schemas
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class RudasResponseSubmit(BaseModel):
    """A single domain response submission."""
    domain: str = Field(..., max_length=50)
    question_number: int
    response_value: Optional[str] = None
    score: float = Field(..., ge=0)
    max_score: float = Field(..., gt=0)
    notes: Optional[str] = None


class RudasAssessmentSubmit(BaseModel):
    """Submit the full RUDAS assessment with all domain responses."""
    responses: List[RudasResponseSubmit]


class RudasResponseOut(BaseModel):
    id: UUID
    domain: str
    question_number: int
    response_value: Optional[str] = None
    score: float
    max_score: float
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class RudasAssessmentOut(BaseModel):
    id: UUID
    patient_profile_id: UUID
    total_score: Optional[float] = None
    max_possible_score: int
    version: str
    is_completed: bool
    assessment_date: datetime
    responses: List[RudasResponseOut] = []

    class Config:
        from_attributes = True

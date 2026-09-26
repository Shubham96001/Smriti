from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class RelationshipRequest(BaseModel):
    patient_email: EmailStr


class RelationshipDecision(BaseModel):
    approved: bool


class RelationshipOut(BaseModel):
    id: UUID
    patient_name: str
    caregiver_name: str
    status: str
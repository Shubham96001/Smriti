"""
SmritiSaathi — Memory Schemas
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class MemoryItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(default="general", max_length=50)
    # image_path and voice_note_path handled by file upload endpoints


class MemoryItemUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)


class MemoryItemOut(BaseModel):
    id: UUID
    patient_profile_id: UUID
    created_by_user_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    category: str
    image_path: Optional[str] = None
    voice_note_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MemoryListResponse(BaseModel):
    items: List[MemoryItemOut] = []
    total: int = 0

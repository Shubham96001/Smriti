from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class AssessmentResponseIn(BaseModel):
    session_id: UUID
    item_id: UUID
    response_text: str = Field(min_length=1, max_length=1000)
    score: int | None = Field(default=None, ge=0, le=100)


class AssessmentItem(BaseModel):
    id: UUID
    item_number: int
    prompt: str
    response_options: list[Any]
    version: str


class AssessmentStatus(BaseModel):
    baseline_completed: bool
    session_id: UUID | None = None
    completed_items: int = 0
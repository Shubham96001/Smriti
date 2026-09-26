from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class MemoryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    body: str = Field(default="", max_length=4000)
    image_url: str | None = Field(default=None, max_length=2000)


class MemoryItem(MemoryCreate):
    id: UUID
    created_at: datetime
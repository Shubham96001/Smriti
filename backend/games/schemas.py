from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SessionStart(BaseModel):
    game_id: str = "memory_match"


class GameEventIn(BaseModel):
    event_id: UUID
    event_type: str = Field(min_length=1, max_length=80)
    payload: dict[str, Any] = Field(default_factory=dict)


class EventsBatch(BaseModel):
    events: list[GameEventIn] = Field(max_length=200)


class SessionComplete(BaseModel):
    result: dict[str, Any] = Field(default_factory=dict)
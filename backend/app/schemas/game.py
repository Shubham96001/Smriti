"""
SmritiSaathi — Game Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field


class GameEventSubmit(BaseModel):
    event_type: str = Field(..., max_length=50)
    event_data: Optional[Dict[str, Any]] = None
    response_time_ms: Optional[int] = None
    is_correct: Optional[bool] = None


class StartGameRequest(BaseModel):
    game_type: str = Field(..., max_length=50)
    difficulty_level: Optional[int] = Field(default=None, ge=1, le=10)


class EndGameRequest(BaseModel):
    total_score: int = 0
    max_score: int = 0
    accuracy: float = Field(default=0.0, ge=0, le=1)
    avg_response_time_ms: Optional[int] = None
    hints_used: int = 0
    events: List[GameEventSubmit] = []


class GameSessionOut(BaseModel):
    id: UUID
    game_type: str
    difficulty_level: int
    total_score: int
    max_score: int
    accuracy: float
    avg_response_time_ms: Optional[int] = None
    hints_used: int
    is_completed: bool
    started_at: datetime
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GameHistoryResponse(BaseModel):
    sessions: List[GameSessionOut] = []
    total_played: int = 0
    average_accuracy: Optional[float] = None


class AdaptiveDifficultyResponse(BaseModel):
    """The difficulty recommendation for the next game session."""
    game_type: str
    recommended_difficulty: int
    reason: str
    parameters: Dict[str, Any] = {}

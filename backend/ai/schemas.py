from typing import Any

from pydantic import BaseModel, Field


class PerformanceEvidence(BaseModel):
    current_level: int = Field(ge=1, le=5)
    recent_accuracies: list[float] = Field(default_factory=list, max_length=10)
    recent_hints: list[int] = Field(default_factory=list, max_length=10)


class AdaptiveDecision(BaseModel):
    level: int
    reason: str
    metrics: dict[str, Any]
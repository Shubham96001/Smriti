"""
SmritiSaathi — Game Models

Tracks game sessions, individual events, and adaptive difficulty decisions.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Uuid, JSON, JSON, String, Integer, Float, Boolean, DateTime, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class GameSession(Base):
    """
    A single game play session.
    Stores aggregate metrics for the session.
    """
    __tablename__ = "game_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    game_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # memory_matching, pattern_sequence, attention, daily_routine
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)
    total_score: Mapped[int] = mapped_column(Integer, default=0)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    avg_response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile", back_populates="game_sessions"
    )
    events: Mapped[list["GameEvent"]] = relationship(
        "GameEvent", back_populates="session",
        cascade="all, delete-orphan", lazy="select",
    )

    def __repr__(self) -> str:
        return f"<GameSession {self.game_type} difficulty={self.difficulty_level}>"


class GameEvent(Base):
    """Individual event within a game session (answer, hint use, etc.)."""
    __tablename__ = "game_events"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("game_sessions.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # answer, hint, timeout, skip
    event_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    session: Mapped["GameSession"] = relationship(
        "GameSession", back_populates="events"
    )

    def __repr__(self) -> str:
        return f"<GameEvent {self.event_type} correct={self.is_correct}>"


class DifficultyDecision(Base):
    """
    Records each adaptive difficulty adjustment with its rationale.
    Enables review and improvement of the adaptation algorithm.
    """
    __tablename__ = "difficulty_decisions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    game_type: Mapped[str] = mapped_column(String(50), nullable=False)
    previous_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    new_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    metrics_snapshot: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<DifficultyDecision {self.game_type} {self.previous_difficulty}->{self.new_difficulty}>"

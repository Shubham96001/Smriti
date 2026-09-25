"""
SmritiSaathi — RUDAS Assessment Models

Stores baseline assessments and individual domain responses.
Uses the approved 6-domain RUDAS structure with max score of 30.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Uuid, JSON, String, Integer, Float, Boolean, DateTime, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RudasAssessment(Base):
    """
    A single RUDAS assessment session for a patient.
    Each patient should have at most one completed baseline.
    """
    __tablename__ = "rudas_assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    total_score: Mapped[float] = mapped_column(Float, nullable=True)
    max_possible_score: Mapped[int] = mapped_column(Integer, default=30)
    version: Mapped[str] = mapped_column(String(10), default="1.0")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    assessment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile", back_populates="assessments"
    )
    responses: Mapped[list["RudasResponse"]] = relationship(
        "RudasResponse", back_populates="assessment",
        cascade="all, delete-orphan", lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<RudasAssessment score={self.total_score} completed={self.is_completed}>"


class RudasResponse(Base):
    """
    Individual response for each RUDAS domain/question.

    RUDAS domains:
    1. Body orientation (max 5)
    2. Praxis (max 2)
    3. Drawing (max 3)
    4. Judgement (max 4)
    5. Memory recall (max 8)
    6. Language (max 8)
    """
    __tablename__ = "rudas_responses"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("rudas_assessments.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    domain: Mapped[str] = mapped_column(String(50), nullable=False)
    question_number: Mapped[int] = mapped_column(Integer, nullable=False)
    response_value: Mapped[str] = mapped_column(Text, nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    max_score: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    assessment: Mapped["RudasAssessment"] = relationship(
        "RudasAssessment", back_populates="responses"
    )

    def __repr__(self) -> str:
        return f"<RudasResponse domain={self.domain} q={self.question_number} score={self.score}>"

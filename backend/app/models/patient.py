"""
SmritiSaathi — Patient Profile Model

Patient-specific information linked to the users table.
Tracks baseline assessment completion for login routing.
"""

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Uuid, JSON, String, Boolean, Date, DateTime, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    emergency_contact_name: Mapped[str] = mapped_column(String(255), nullable=True)
    emergency_contact_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    consent_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    baseline_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="patient_profile")
    caregiver_links: Mapped[list["PatientCaregiverLink"]] = relationship(
        "PatientCaregiverLink", back_populates="patient", lazy="select"
    )
    assessments: Mapped[list["RudasAssessment"]] = relationship(
        "RudasAssessment", back_populates="patient", lazy="select"
    )
    game_sessions: Mapped[list["GameSession"]] = relationship(
        "GameSession", back_populates="patient", lazy="select"
    )
    memory_items: Mapped[list["MemoryItem"]] = relationship(
        "MemoryItem", back_populates="patient", lazy="select"
    )
    reminders: Mapped[list["Reminder"]] = relationship(
        "Reminder", back_populates="patient", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<PatientProfile {self.full_name}>"

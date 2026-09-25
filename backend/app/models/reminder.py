"""
SmritiSaathi — Reminder Models

Supports medicine, hydration, meals, activities, appointments.
Tracks completion, postponement, and missed status.
"""

import uuid
from datetime import datetime, time, timezone

from sqlalchemy import Uuid, JSON, String, Boolean, DateTime, Time, ForeignKey, Text, Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base


class ReminderType(str, enum.Enum):
    MEDICINE = "medicine"
    HYDRATION = "hydration"
    MEAL = "meal"
    ACTIVITY = "activity"
    APPOINTMENT = "appointment"
    ROUTINE = "routine"
    OTHER = "other"


class Recurrence(str, enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    reminder_type: Mapped[ReminderType] = mapped_column(
        SAEnum(ReminderType, name="reminder_type", create_constraint=True),
        default=ReminderType.OTHER,
    )
    schedule_time: Mapped[time] = mapped_column(Time, nullable=False)
    recurrence: Mapped[Recurrence] = mapped_column(
        SAEnum(Recurrence, name="recurrence_type", create_constraint=True),
        default=Recurrence.DAILY,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile", back_populates="reminders"
    )
    events: Mapped[list["ReminderEvent"]] = relationship(
        "ReminderEvent", back_populates="reminder",
        cascade="all, delete-orphan", lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Reminder '{self.title}' type={self.reminder_type}>"


class ReminderEventStatus(str, enum.Enum):
    COMPLETED = "completed"
    POSTPONED = "postponed"
    MISSED = "missed"


class ReminderEvent(Base):
    """Records what happened when a reminder was due."""
    __tablename__ = "reminder_events"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    reminder_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("reminders.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    status: Mapped[ReminderEventStatus] = mapped_column(
        SAEnum(ReminderEventStatus, name="reminder_event_status", create_constraint=True),
        nullable=False,
    )
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    reminder: Mapped["Reminder"] = relationship(
        "Reminder", back_populates="events"
    )

    def __repr__(self) -> str:
        return f"<ReminderEvent {self.status}>"

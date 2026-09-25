"""
SmritiSaathi — Audit Log & Caregiver Alert Models

Audit logs track security-relevant actions.
Caregiver alerts are monitoring notifications, not medical diagnoses.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Uuid, JSON, JSON, String, Boolean, DateTime, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.caregiver import CaregiverProfile

from app.core.database import Base


class AuditLog(Base):
    """Records important security and data actions for accountability."""
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[str] = mapped_column(String(50), nullable=True)
    details: Mapped[dict] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} by user={self.user_id}>"


class CaregiverAlert(Base):
    """
    Monitoring alerts for caregivers.
    Uses descriptive language, not medical diagnoses.

    Example alert types:
    - lower_activity: "Lower activity this week"
    - reminder_missed: "Reminder missed"
    - assistance_requested: "More assistance requested"
    - performance_variation: "Performance variation observed"
    """
    __tablename__ = "caregiver_alerts"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    caregiver_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("caregiver_profiles.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    caregiver: Mapped["CaregiverProfile"] = relationship(
        "CaregiverProfile", back_populates="alerts"
    )

    def __repr__(self) -> str:
        return f"<CaregiverAlert {self.alert_type} read={self.is_read}>"

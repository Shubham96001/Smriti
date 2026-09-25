"""
SmritiSaathi — Caregiver Profile & Patient-Caregiver Link Models

Caregivers have separate profiles and must be explicitly linked
to patients via invitation codes. No automatic access.
"""

import uuid
import secrets
from datetime import datetime, timezone

from sqlalchemy import Uuid, JSON, String, Boolean, DateTime, ForeignKey, Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base


class CaregiverProfile(Base):
    __tablename__ = "caregiver_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=True)
    consent_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    invitation_code: Mapped[str] = mapped_column(
        String(12), unique=True, nullable=False,
        default=lambda: secrets.token_hex(6).upper()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="caregiver_profile")
    patient_links: Mapped[list["PatientCaregiverLink"]] = relationship(
        "PatientCaregiverLink", back_populates="caregiver", lazy="select"
    )
    alerts: Mapped[list["CaregiverAlert"]] = relationship(
        "CaregiverAlert", back_populates="caregiver", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<CaregiverProfile {self.full_name}>"


class LinkStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REVOKED = "revoked"


class PatientCaregiverLink(Base):
    __tablename__ = "patient_caregiver_links"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    caregiver_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("caregiver_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[LinkStatus] = mapped_column(
        SAEnum(LinkStatus, name="link_status", create_constraint=True),
        default=LinkStatus.ACTIVE,
    )
    linked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile", back_populates="caregiver_links"
    )
    caregiver: Mapped["CaregiverProfile"] = relationship(
        "CaregiverProfile", back_populates="patient_links"
    )

    def __repr__(self) -> str:
        return f"<Link patient={self.patient_profile_id} caregiver={self.caregiver_profile_id}>"

"""
SmritiSaathi — User Model

Core authentication table. Stores credentials and role.
Every patient and caregiver has exactly one user record.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Uuid, JSON, String, Boolean, DateTime, Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.patient import PatientProfile
    from app.models.caregiver import CaregiverProfile
    from app.models.audit import AuditLog

from app.core.database import Base


class UserRole(str, enum.Enum):
    PATIENT = "patient"
    CAREGIVER = "caregiver"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role", create_constraint=True),
        nullable=False,
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
    patient_profile: Mapped["PatientProfile"] = relationship(
        "PatientProfile", back_populates="user", uselist=False, lazy="selectin"
    )
    caregiver_profile: Mapped["CaregiverProfile"] = relationship(
        "CaregiverProfile", back_populates="user", uselist=False, lazy="selectin"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="user", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<User {self.email} role={self.role}>"

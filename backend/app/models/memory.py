"""
SmritiSaathi — Memory Item Model

Stores memory aids: family photos, names, places, routines.
Items can be created by the patient or an authorized caregiver.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Uuid, JSON, String, DateTime, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MemoryItem(Base):
    __tablename__ = "memory_items"

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
    category: Mapped[str] = mapped_column(
        String(50), default="general"
    )  # family, place, routine, object, other
    image_path: Mapped[str] = mapped_column(String(500), nullable=True)
    voice_note_path: Mapped[str] = mapped_column(String(500), nullable=True)
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
        "PatientProfile", back_populates="memory_items"
    )

    def __repr__(self) -> str:
        return f"<MemoryItem '{self.title}' category={self.category}>"

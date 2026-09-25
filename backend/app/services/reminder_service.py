"""
SmritiSaathi — Reminder Service
"""

from datetime import datetime, date, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reminder import Reminder, ReminderEvent, ReminderEventStatus
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderEventCreate


async def create_reminder(
    patient_profile_id: UUID,
    created_by_user_id: UUID,
    data: ReminderCreate,
    db: AsyncSession,
) -> Reminder:
    """Create a new reminder."""
    reminder = Reminder(
        patient_profile_id=patient_profile_id,
        created_by_user_id=created_by_user_id,
        title=data.title,
        description=data.description,
        reminder_type=data.reminder_type,
        schedule_time=data.schedule_time,
        recurrence=data.recurrence,
        is_active=True,
    )
    db.add(reminder)
    await db.flush()
    return reminder


async def get_reminders(
    patient_profile_id: UUID,
    is_active: Optional[bool],
    db: AsyncSession,
) -> List[Reminder]:
    """Get reminders for a patient."""
    query = select(Reminder).where(
        Reminder.patient_profile_id == patient_profile_id
    )
    if is_active is not None:
        query = query.where(Reminder.is_active == is_active)
    query = query.order_by(Reminder.schedule_time)

    result = await db.execute(query)
    return list(result.scalars().all())


async def update_reminder(
    reminder_id: UUID,
    patient_profile_id: UUID,
    data: ReminderUpdate,
    db: AsyncSession,
) -> Reminder:
    """Update an existing reminder."""
    result = await db.execute(
        select(Reminder).where(
            Reminder.id == reminder_id,
            Reminder.patient_profile_id == patient_profile_id,
        )
    )
    reminder = result.scalar_one_or_none()
    if reminder is None:
        raise ValueError("Reminder not found")

    if data.title is not None:
        reminder.title = data.title
    if data.description is not None:
        reminder.description = data.description
    if data.reminder_type is not None:
        reminder.reminder_type = data.reminder_type
    if data.schedule_time is not None:
        reminder.schedule_time = data.schedule_time
    if data.recurrence is not None:
        reminder.recurrence = data.recurrence
    if data.is_active is not None:
        reminder.is_active = data.is_active

    await db.flush()
    return reminder


async def record_reminder_event(
    reminder_id: UUID,
    patient_profile_id: UUID,
    data: ReminderEventCreate,
    db: AsyncSession,
) -> ReminderEvent:
    """Record that a reminder was completed, postponed, or missed."""
    # First verify ownership
    result = await db.execute(
        select(Reminder).where(
            Reminder.id == reminder_id,
            Reminder.patient_profile_id == patient_profile_id,
        )
    )
    reminder = result.scalar_one_or_none()
    if reminder is None:
        raise ValueError("Reminder not found")

    event = ReminderEvent(
        reminder_id=reminder.id,
        status=data.status,
        notes=data.notes,
    )
    db.add(event)
    await db.flush()
    return event


async def get_active_reminders_count(
    patient_profile_id: UUID, db: AsyncSession
) -> int:
    """Count active reminders for a patient."""
    result = await db.execute(
        select(func.count(Reminder.id)).where(
            Reminder.patient_profile_id == patient_profile_id,
            Reminder.is_active == True,
        )
    )
    return result.scalar() or 0


async def get_missed_reminders_count_last_week(
    patient_profile_id: UUID, db: AsyncSession
) -> int:
    """Count missed reminders in the last 7 days for caregiver dashboard."""
    from datetime import timedelta
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    query = (
        select(func.count(ReminderEvent.id))
        .join(Reminder)
        .where(
            Reminder.patient_profile_id == patient_profile_id,
            ReminderEvent.status == ReminderEventStatus.MISSED,
            ReminderEvent.event_time >= seven_days_ago,
        )
    )
    result = await db.execute(query)
    return result.scalar() or 0

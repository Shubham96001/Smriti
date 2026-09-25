"""
SmritiSaathi — Memory Service
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import MemoryItem
from app.schemas.memory import MemoryItemCreate, MemoryItemUpdate


async def create_memory_item(
    patient_profile_id: UUID,
    created_by_user_id: UUID,
    data: MemoryItemCreate,
    db: AsyncSession,
) -> MemoryItem:
    """Create a new memory item (by patient or authorized caregiver)."""
    item = MemoryItem(
        patient_profile_id=patient_profile_id,
        created_by_user_id=created_by_user_id,
        title=data.title,
        description=data.description,
        category=data.category,
    )
    db.add(item)
    await db.flush()
    return item


async def get_memory_items(
    patient_profile_id: UUID,
    category: Optional[str],
    db: AsyncSession,
) -> List[MemoryItem]:
    """Get all memory items for a patient, optionally filtered by category."""
    query = select(MemoryItem).where(
        MemoryItem.patient_profile_id == patient_profile_id
    )
    if category:
        query = query.where(MemoryItem.category == category)
    query = query.order_by(MemoryItem.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


async def update_memory_item(
    item_id: UUID,
    patient_profile_id: UUID,
    data: MemoryItemUpdate,
    db: AsyncSession,
) -> MemoryItem:
    """Update an existing memory item."""
    result = await db.execute(
        select(MemoryItem).where(
            MemoryItem.id == item_id,
            MemoryItem.patient_profile_id == patient_profile_id,
        )
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise ValueError("Memory item not found")

    if data.title is not None:
        item.title = data.title
    if data.description is not None:
        item.description = data.description
    if data.category is not None:
        item.category = data.category

    await db.flush()
    return item


async def delete_memory_item(
    item_id: UUID, patient_profile_id: UUID, db: AsyncSession
) -> bool:
    """Delete a memory item."""
    result = await db.execute(
        select(MemoryItem).where(
            MemoryItem.id == item_id,
            MemoryItem.patient_profile_id == patient_profile_id,
        )
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise ValueError("Memory item not found")

    await db.delete(item)
    await db.flush()
    return True


async def count_memory_items(
    patient_profile_id: UUID, db: AsyncSession
) -> int:
    """Count total memory items for a patient."""
    result = await db.execute(
        select(func.count(MemoryItem.id)).where(
            MemoryItem.patient_profile_id == patient_profile_id
        )
    )
    return result.scalar() or 0

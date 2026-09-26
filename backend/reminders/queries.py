from typing import Any
from uuid import UUID, uuid4

from database import execute_returning, fetch_all


def list_reminders(patient_id: UUID) -> list[dict[str, Any]]:
    return fetch_all("SELECT id, title, description, remind_at, recurrence, is_active FROM reminders WHERE patient_id = %s ORDER BY remind_at", (patient_id,))


def create_reminder(patient_id: UUID, user_id: UUID, title: str, description: str, remind_at: Any, recurrence: str) -> dict[str, Any] | None:
    return execute_returning(
        "INSERT INTO reminders (id, patient_id, title, description, remind_at, recurrence, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id, title, description, remind_at, recurrence, is_active",
        (uuid4(), patient_id, title, description, remind_at, recurrence, user_id),
    )
from typing import Any
from uuid import UUID

from database import fetch_one


def patient_summary(patient_id: UUID) -> dict[str, Any]:
    counts = fetch_one(
        """SELECT
             (SELECT COUNT(*) FROM game_sessions WHERE patient_id = %s AND completed_at IS NOT NULL) AS games_completed,
             (SELECT COUNT(*) FROM memory_items WHERE patient_id = %s) AS memory_items,
             (SELECT COUNT(*) FROM reminders WHERE patient_id = %s AND is_active) AS active_reminders""",
        (patient_id, patient_id, patient_id),
    )
    return counts or {"games_completed": 0, "memory_items": 0, "active_reminders": 0}
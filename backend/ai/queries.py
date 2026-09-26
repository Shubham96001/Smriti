from typing import Any
from uuid import UUID

from database import fetch_all


def recent_activity(patient_id: UUID) -> list[dict[str, Any]]:
    return fetch_all(
        "SELECT game_id, difficulty, started_at, completed_at FROM game_sessions WHERE patient_id = %s ORDER BY started_at DESC LIMIT 10",
        (patient_id,),
    )
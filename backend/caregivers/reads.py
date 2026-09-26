from typing import Any
from uuid import UUID

from database import fetch_all


def caregiver_patients(user_id: UUID) -> list[dict[str, Any]]:
    return fetch_all(
        """SELECT p.id, p.full_name, r.status FROM caregiver_relationships r
           JOIN caregiver_profiles c ON c.id = r.caregiver_id
           JOIN patient_profiles p ON p.id = r.patient_id
           WHERE c.user_id = %s ORDER BY p.full_name""",
        (user_id,),
    )


def patient_activity(patient_id: UUID) -> list[dict[str, Any]]:
    return fetch_all(
        "SELECT game_id, started_at, completed_at FROM game_sessions WHERE patient_id = %s ORDER BY started_at DESC LIMIT 20",
        (patient_id,),
    )
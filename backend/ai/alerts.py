from typing import Any
from uuid import UUID, uuid4

from database import execute_returning, fetch_all


def list_alerts(patient_id: UUID) -> list[dict[str, Any]]:
    return fetch_all(
        "SELECT id, alert_type, message, is_read, created_at FROM caregiver_alerts WHERE patient_id = %s ORDER BY created_at DESC LIMIT 50",
        (patient_id,),
    )


def create_alert(patient_id: UUID, caregiver_id: UUID | None, alert_type: str, message: str) -> dict[str, Any] | None:
    return execute_returning(
        "INSERT INTO caregiver_alerts (id, patient_id, caregiver_id, alert_type, message) VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at",
        (uuid4(), patient_id, caregiver_id, alert_type, message),
    )
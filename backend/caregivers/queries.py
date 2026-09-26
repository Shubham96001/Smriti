from typing import Any
from uuid import UUID, uuid4

from database import execute_returning, fetch_all, fetch_one


def request_relationship(caregiver_user_id: UUID, patient_email: str) -> dict[str, Any] | None:
    row = fetch_one(
        "SELECT p.id AS patient_id, c.id AS caregiver_id FROM patient_profiles p JOIN users u ON u.id = p.user_id CROSS JOIN caregiver_profiles c WHERE u.email = %s AND c.user_id = %s",
        (patient_email.lower(), caregiver_user_id),
    )
    if row is None:
        return None
    return execute_returning(
        "INSERT INTO caregiver_relationships (id, patient_id, caregiver_id) VALUES (%s, %s, %s) ON CONFLICT (patient_id, caregiver_id) DO UPDATE SET status = 'pending', requested_at = CURRENT_TIMESTAMP RETURNING id, status",
        (uuid4(), row["patient_id"], row["caregiver_id"]),
    )


def list_pending_for_patient(patient_user_id: UUID) -> list[dict[str, Any]]:
    return fetch_all(
        """SELECT r.id, c.full_name AS caregiver_name, r.status FROM caregiver_relationships r
           JOIN patient_profiles p ON p.id = r.patient_id
           JOIN caregiver_profiles c ON c.id = r.caregiver_id
           WHERE p.user_id = %s AND r.status = 'pending' ORDER BY r.requested_at""",
        (patient_user_id,),
    )


def decide_relationship(patient_user_id: UUID, relationship_id: UUID, approved: bool) -> dict[str, Any] | None:
    return execute_returning(
        """UPDATE caregiver_relationships r SET status = %s, approved_at = CASE WHEN %s THEN CURRENT_TIMESTAMP ELSE NULL END
           FROM patient_profiles p WHERE r.patient_id = p.id AND p.user_id = %s AND r.id = %s AND r.status = 'pending'
           RETURNING r.id, r.status""",
        ("approved" if approved else "revoked", approved, patient_user_id, relationship_id),
    )
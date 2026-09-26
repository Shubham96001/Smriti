from uuid import UUID

from fastapi import HTTPException

from database import fetch_one


def assert_approved_caregiver(caregiver_user_id: UUID, patient_id: UUID) -> None:
    row = fetch_one(
        """SELECT 1 FROM caregiver_relationships r
           JOIN caregiver_profiles c ON c.id = r.caregiver_id
           WHERE c.user_id = %s AND r.patient_id = %s AND r.status = 'approved'""",
        (caregiver_user_id, patient_id),
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Patient not found")


def assert_hcw_scope(hcw_user_id: UUID, patient_id: UUID) -> None:
    row = fetch_one(
        """SELECT 1 FROM hcw_scopes s JOIN hcw_profiles h ON h.id = s.hcw_id
           WHERE h.user_id = %s AND s.patient_id = %s AND s.status = 'approved'""",
        (hcw_user_id, patient_id),
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Patient not found")
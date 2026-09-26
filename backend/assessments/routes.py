from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from assessments import queries
from assessments.schemas import AssessmentResponseIn, AssessmentStatus
from dependencies import require_role

router = APIRouter(prefix="/assessments", tags=["assessments"])


def _patient_id(user: dict[str, Any]) -> UUID:
    patient_id = queries.patient_id_for_user(user["id"])
    if patient_id is None:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient_id


@router.get("/rudas/status", response_model=AssessmentStatus)
def status(user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    return queries.assessment_status(_patient_id(user))


@router.post("/rudas/start")
def start(user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    patient_id = _patient_id(user)
    state = queries.assessment_status(patient_id)
    if state["baseline_completed"]:
        raise HTTPException(status_code=409, detail="Baseline is already completed")
    return queries.start_assessment(patient_id)


@router.post("/rudas")
def save_response(
    data: AssessmentResponseIn,
    user: dict[str, Any] = Depends(require_role("patient")),
) -> dict[str, bool]:
    result = queries.save_response(_patient_id(user), data.session_id, data.item_id, data.response_text, data.score)
    if result.get("not_found"):
        raise HTTPException(status_code=404, detail="Assessment session not found")
    return result
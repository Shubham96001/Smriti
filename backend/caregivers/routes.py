from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from caregivers import queries, reads
from caregivers.access import assert_approved_caregiver
from caregivers.schemas import RelationshipDecision, RelationshipRequest
from dependencies import require_role
from users.queries import get_user_public

router = APIRouter(prefix="/caregivers", tags=["caregivers"])


@router.post("/relationships/request", status_code=201)
def request_link(data: RelationshipRequest, user: dict[str, Any] = Depends(require_role("caregiver"))) -> dict[str, Any]:
    result = queries.request_relationship(user["id"], str(data.patient_email))
    if result is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return result


@router.get("/relationships")
def relationships(user: dict[str, Any] = Depends(require_role("caregiver"))) -> list[dict[str, Any]]:
    return reads.caregiver_patients(user["id"])


@router.get("/approvals")
def approvals(user: dict[str, Any] = Depends(require_role("patient"))) -> list[dict[str, Any]]:
    return queries.list_pending_for_patient(user["id"])


@router.post("/approvals/{relationship_id}")
def decide(relationship_id: UUID, data: RelationshipDecision, user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    result = queries.decide_relationship(user["id"], relationship_id, data.approved)
    if result is None:
        raise HTTPException(status_code=404, detail="Approval request not found")
    return result


@router.get("/patients/{patient_id}/activity")
def scoped_activity(patient_id: UUID, user: dict[str, Any] = Depends(require_role("caregiver"))) -> list[dict[str, Any]]:
    assert_approved_caregiver(user["id"], patient_id)
    return reads.patient_activity(patient_id)
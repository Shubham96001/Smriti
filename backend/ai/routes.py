from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ai.alerts import list_alerts
from ai.adaptive_engine import choose_difficulty
from ai.analytics import patient_summary
from ai.queries import recent_activity
from ai.schemas import PerformanceEvidence
from dependencies import require_role

router = APIRouter(prefix="/ai", tags=["activity"])


def _patient_id(user: dict[str, Any]) -> UUID:
    from database import fetch_one
    row = fetch_one("SELECT id FROM patient_profiles WHERE user_id = %s", (user["id"],))
    if row is None:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return row["id"]


@router.get("/summary")
def summary(user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    patient_id = _patient_id(user)
    return {**patient_summary(patient_id), "recent_activity": recent_activity(patient_id)}


@router.get("/alerts")
def alerts(user: dict[str, Any] = Depends(require_role("patient"))) -> list[dict[str, Any]]:
    return list_alerts(_patient_id(user))


@router.post("/difficulty")
def difficulty(data: PerformanceEvidence, _: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    return choose_difficulty(data.current_level, data.recent_accuracies, data.recent_hints)
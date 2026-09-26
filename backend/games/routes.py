from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from dependencies import require_role
from games import queries
from games.schemas import EventsBatch, SessionComplete, SessionStart

router = APIRouter(prefix="/games", tags=["games"])


def _patient_id(user: dict[str, Any]) -> UUID:
    patient_id = queries.patient_id_for_user(user["id"])
    if patient_id is None:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient_id


@router.get("")
def games(_: dict[str, Any] = Depends(require_role("patient"))) -> list[dict[str, Any]]:
    return queries.list_games()


@router.post("/sessions", status_code=201)
def start_session(data: SessionStart, user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    session = queries.create_session(_patient_id(user), data.game_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return session


@router.post("/sessions/{session_id}/events")
def add_events(session_id: UUID, data: EventsBatch, user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, int]:
    patient_id = _patient_id(user)
    if not queries.owns_session(session_id, patient_id):
        raise HTTPException(status_code=404, detail="Game session not found")
    inserted = queries.add_events(session_id, [event.model_dump() for event in data.events])
    return {"accepted": inserted}


@router.post("/sessions/{session_id}/complete")
def complete(session_id: UUID, data: SessionComplete, user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    if not queries.owns_session(session_id, _patient_id(user)):
        raise HTTPException(status_code=404, detail="Game session not found")
    result = queries.complete_session(session_id, data.result)
    if result is None:
        raise HTTPException(status_code=409, detail="Game session is already complete")
    return result
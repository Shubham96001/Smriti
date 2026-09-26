from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from database import fetch_one
from dependencies import require_role
from reminders.queries import create_reminder, list_reminders
from reminders.schemas import ReminderCreate

router = APIRouter(prefix="/reminders", tags=["reminders"])


def _patient_id(user: dict[str, Any]) -> UUID:
    row = fetch_one("SELECT id FROM patient_profiles WHERE user_id = %s", (user["id"],))
    if row is None:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return row["id"]


@router.get("")
def get_reminders(user: dict[str, Any] = Depends(require_role("patient"))) -> list[dict[str, Any]]:
    return list_reminders(_patient_id(user))


@router.post("", status_code=201)
def add_reminder(data: ReminderCreate, user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    reminder = create_reminder(_patient_id(user), user["id"], data.title, data.description, data.remind_at, data.recurrence)
    if reminder is None:
        raise HTTPException(status_code=500, detail="Unable to save reminder")
    return reminder
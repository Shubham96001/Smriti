from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from database import fetch_one
from dependencies import require_role
from memory.queries import create_item, list_items
from memory.schemas import MemoryCreate

router = APIRouter(prefix="/memory", tags=["memory"])


def _patient_id(user: dict[str, Any]) -> UUID:
    row = fetch_one("SELECT id FROM patient_profiles WHERE user_id = %s", (user["id"],))
    if row is None:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return row["id"]


@router.get("")
def get_items(user: dict[str, Any] = Depends(require_role("patient"))) -> list[dict[str, Any]]:
    return list_items(_patient_id(user))


@router.post("", status_code=201)
def add_item(data: MemoryCreate, user: dict[str, Any] = Depends(require_role("patient"))) -> dict[str, Any]:
    item = create_item(_patient_id(user), user["id"], data.title, data.body, data.image_url)
    if item is None:
        raise HTTPException(status_code=500, detail="Unable to save memory item")
    return item
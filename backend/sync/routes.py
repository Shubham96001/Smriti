from typing import Any

from fastapi import APIRouter, Depends

from dependencies import get_current_user
from sync.schemas import SyncBatch
from sync.service import synchronize

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("")
def sync(data: SyncBatch, user: dict[str, Any] = Depends(get_current_user)) -> dict[str, int]:
    return synchronize(user["id"], [record.model_dump() for record in data.records])
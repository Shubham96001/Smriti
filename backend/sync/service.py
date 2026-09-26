from typing import Any
from uuid import UUID

from sync.queries import save_records


def synchronize(user_id: UUID, records: list[dict[str, Any]]) -> dict[str, int]:
    return {"accepted": save_records(user_id, records)}
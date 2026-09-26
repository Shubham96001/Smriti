from typing import Any
from pydantic import BaseModel, Field


class SyncRecord(BaseModel):
    client_record_id: str = Field(min_length=1, max_length=200)
    resource_type: str = Field(min_length=1, max_length=80)
    payload: dict[str, Any]


class SyncBatch(BaseModel):
    records: list[SyncRecord] = Field(max_length=200)
from typing import Any
from uuid import UUID, uuid4

from psycopg.types.json import Jsonb

from database import execute_query


def save_records(user_id: UUID, records: list[dict[str, Any]]) -> int:
    saved = 0
    for record in records:
        saved += execute_query(
            "INSERT INTO offline_sync_records (id, user_id, client_record_id, resource_type, payload) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id, client_record_id) DO NOTHING",
            (uuid4(), user_id, record["client_record_id"], record["resource_type"], Jsonb(record["payload"])),
        )
    return saved
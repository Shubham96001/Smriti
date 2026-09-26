from typing import Any
from uuid import UUID, uuid4

from database import execute_returning, fetch_all


def list_items(patient_id: UUID) -> list[dict[str, Any]]:
    return fetch_all("SELECT id, title, body, image_url, created_at FROM memory_items WHERE patient_id = %s ORDER BY created_at DESC", (patient_id,))


def create_item(patient_id: UUID, user_id: UUID, title: str, body: str, image_url: str | None) -> dict[str, Any] | None:
    return execute_returning(
        "INSERT INTO memory_items (id, patient_id, title, body, image_url, created_by) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, title, body, image_url, created_at",
        (uuid4(), patient_id, title, body, image_url, user_id),
    )
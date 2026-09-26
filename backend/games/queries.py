from typing import Any
from uuid import UUID, uuid4

from psycopg.types.json import Jsonb

from database import execute_query, execute_returning, fetch_all, fetch_one


def patient_id_for_user(user_id: UUID) -> UUID | None:
    row = fetch_one("SELECT id FROM patient_profiles WHERE user_id = %s", (user_id,))
    return row["id"] if row else None


def create_session(patient_id: UUID, game_id: str) -> dict[str, Any] | None:
    game = fetch_one("SELECT id FROM games WHERE id = %s AND is_active", (game_id,))
    if game is None:
        return None
    row = execute_returning(
        "INSERT INTO game_sessions (id, patient_id, game_id) VALUES (%s, %s, %s) RETURNING id, game_id, difficulty, started_at",
        (uuid4(), patient_id, game_id),
    )
    return row


def owns_session(session_id: UUID, patient_id: UUID) -> bool:
    return fetch_one("SELECT id FROM game_sessions WHERE id = %s AND patient_id = %s", (session_id, patient_id)) is not None


def add_events(session_id: UUID, events: list[dict[str, Any]]) -> int:
    def insert_event(event: dict[str, Any]) -> None:
        execute_query(
            "INSERT INTO game_events (id, session_id, event_type, payload) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
            (event["event_id"], session_id, event["event_type"], Jsonb(event["payload"])),
        )
    for event in events:
        insert_event(event)
    return len(events)


def complete_session(session_id: UUID, result: dict[str, Any]) -> dict[str, Any] | None:
    return execute_returning(
        "UPDATE game_sessions SET completed_at = CURRENT_TIMESTAMP, result = %s WHERE id = %s AND completed_at IS NULL RETURNING id, completed_at",
        (Jsonb(result), session_id),
    )


def list_games() -> list[dict[str, Any]]:
    return fetch_all("SELECT id, name FROM games WHERE is_active ORDER BY name")
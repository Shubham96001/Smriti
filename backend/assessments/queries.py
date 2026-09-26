from typing import Any
from uuid import UUID, uuid4

from database import execute_returning, fetch_all, fetch_one


def patient_id_for_user(user_id: UUID) -> UUID | None:
    row = fetch_one("SELECT id FROM patient_profiles WHERE user_id = %s", (user_id,))
    return row["id"] if row else None


def assessment_status(patient_id: UUID) -> dict[str, Any]:
    row = fetch_one(
        "SELECT baseline_completed FROM patient_profiles WHERE id = %s", (patient_id,)
    )
    session = fetch_one(
        "SELECT id FROM assessment_sessions WHERE patient_id = %s AND status = 'in_progress' ORDER BY started_at DESC LIMIT 1",
        (patient_id,),
    )
    count = 0
    if session:
        result = fetch_one(
            "SELECT COUNT(*) AS count FROM assessment_responses WHERE session_id = %s",
            (session["id"],),
        )
        count = result["count"]
    return {
        "baseline_completed": bool(row and row["baseline_completed"]),
        "session_id": session["id"] if session else None,
        "completed_items": count,
    }


def start_assessment(patient_id: UUID) -> dict[str, Any]:
    session = fetch_one(
        "SELECT id FROM assessment_sessions WHERE patient_id = %s AND status = 'in_progress' ORDER BY started_at DESC LIMIT 1",
        (patient_id,),
    )
    if session is None:
        session = execute_returning(
            "INSERT INTO assessment_sessions (id, patient_id) VALUES (%s, %s) RETURNING id",
            (uuid4(), patient_id),
        )
    items = fetch_all(
        "SELECT id, item_number, prompt, response_options, version FROM assessment_items "
        "WHERE assessment_key = %s AND version = %s AND language = %s ORDER BY item_number",
        ("rudas", "placeholder-v1", "en"),
    )
    return {"session_id": session["id"], "items": items, "version": "placeholder-v1"}


def save_response(patient_id: UUID, session_id: UUID, item_id: UUID, text: str, score: int | None) -> dict[str, Any]:
    owned = fetch_one(
        "SELECT id FROM assessment_sessions WHERE id = %s AND patient_id = %s AND status = 'in_progress'",
        (session_id, patient_id),
    )
    if owned is None:
        return {"not_found": True}
    execute_returning(
        """INSERT INTO assessment_responses (id, session_id, item_id, response_text, score)
           VALUES (%s, %s, %s, %s, %s)
           ON CONFLICT (session_id, item_id) DO UPDATE SET
             response_text = EXCLUDED.response_text, score = EXCLUDED.score,
             saved_at = CURRENT_TIMESTAMP RETURNING id""",
        (uuid4(), session_id, item_id, text, score),
    )
    totals = fetch_one(
        "SELECT COUNT(*) AS answered, (SELECT COUNT(*) FROM assessment_items WHERE assessment_key = %s AND version = %s AND language = %s) AS total "
        "FROM assessment_responses WHERE session_id = %s",
        ("rudas", "placeholder-v1", "en", session_id),
    )
    if totals and totals["answered"] >= totals["total"]:
        execute_returning(
            "UPDATE assessment_sessions SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING id",
            (session_id,),
        )
        execute_returning(
            "UPDATE patient_profiles SET baseline_completed = TRUE WHERE id = %s RETURNING id",
            (patient_id,),
        )
    return {"saved": True, "completed": bool(totals and totals["answered"] >= totals["total"])}
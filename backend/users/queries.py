from typing import Any
from uuid import UUID

from database import fetch_one


def get_user_public(user_id: UUID) -> dict[str, Any] | None:
    return fetch_one(
        """SELECT u.id, u.email, u.role, u.is_active, u.created_at,
                  COALESCE(p.full_name, c.full_name, h.full_name, '') AS full_name,
                  p.baseline_completed
           FROM users u
           LEFT JOIN patient_profiles p ON p.user_id = u.id
           LEFT JOIN caregiver_profiles c ON c.user_id = u.id
           LEFT JOIN hcw_profiles h ON h.user_id = u.id
           WHERE u.id = %s""",
        (user_id,),
    )


def get_user_by_email(email: str) -> dict[str, Any] | None:
    return fetch_one("SELECT id, email, password_hash, role, is_active FROM users WHERE email = %s", (email,))
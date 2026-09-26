from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from psycopg.errors import UniqueViolation

from auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UserPublic
from auth.security import create_access_token, hash_password, verify_password
from database import execute_transaction, fetch_one
from dependencies import get_current_user
from users.queries import get_user_public

router = APIRouter(prefix="/auth", tags=["auth"])


def _create_account(connection: Any, data: RegisterRequest, user_id: Any) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO users
               (id, email, password_hash, role, is_active, created_at, updated_at)
               VALUES (%s, %s, %s, %s, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
            (user_id, str(data.email).lower(), hash_password(data.password), data.role),
        )
        if data.role == "patient":
            cursor.execute(
                """INSERT INTO patient_profiles
                   (id, user_id, full_name, date_of_birth, gender, preferred_language,
                    contact_phone, address, consent_acknowledged, baseline_completed,
                    created_at, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE,
                       CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                (uuid4(), user_id, data.full_name, data.date_of_birth, data.gender,
                 data.preferred_language, data.contact_phone, data.address, data.consent_acknowledged),
            )
        elif data.role == "caregiver":
            cursor.execute(
                """INSERT INTO caregiver_profiles
                                     (id, user_id, full_name, contact_phone, relationship_type,
                                        consent_acknowledged, invitation_code, created_at, updated_at)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                (uuid4(), user_id, data.full_name, data.contact_phone, data.relationship_type,
                                 data.consent_acknowledged, uuid4().hex[:8].upper()),
            )
        else:
            cursor.execute(
                "INSERT INTO hcw_profiles (id, user_id, full_name, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
                (uuid4(), user_id, data.full_name),
            )


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: RegisterRequest) -> dict[str, Any]:
    user_id = uuid4()
    try:
        execute_transaction(lambda connection: _create_account(connection, data, user_id))
    except UniqueViolation as exc:
        raise HTTPException(status_code=409, detail="An account with this email already exists") from exc
    user = get_user_public(user_id)
    assert user is not None
    return {"access_token": create_access_token(str(user_id)), "user": user}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest) -> dict[str, Any]:
    account = fetch_one(
        "SELECT id, password_hash, is_active FROM users WHERE email = %s",
        (str(data.email).lower(),),
    )
    if account is None or not verify_password(data.password, account["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not account["is_active"]:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    user = get_user_public(account["id"])
    assert user is not None
    return {"access_token": create_access_token(str(user["id"])), "user": user}


@router.get("/me", response_model=UserPublic)
def me(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    return user
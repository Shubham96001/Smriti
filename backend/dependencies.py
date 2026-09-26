from collections.abc import Callable
from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.security import decode_access_token
from users.queries import get_user_public

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    payload = decode_access_token(credentials.credentials)
    try:
        user_id = UUID(str(payload["sub"])) if payload else None
    except (KeyError, ValueError, TypeError):
        user_id = None
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = get_user_public(user_id)
    if user is None or not user["is_active"]:
        raise HTTPException(status_code=401, detail="Invalid or inactive account")
    return user


def require_role(*roles: str) -> Callable[..., dict[str, Any]]:
    def role_dependency(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user

    return role_dependency
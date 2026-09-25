"""
SmritiSaathi — API Dependencies

Provides FastAPI dependency injection for:
1. Database sessions
2. Current authenticated user
3. Role-based access control
"""

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.models.patient import PatientProfile
from app.models.caregiver import CaregiverProfile, PatientCaregiverLink, LinkStatus

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Decode JWT token, fetch user from DB, verify active status.
    Every protected endpoint uses this dependency.
    """
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


async def require_patient(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency that ensures the current user is a patient."""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient access required",
        )
    return current_user


async def require_caregiver(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency that ensures the current user is a caregiver."""
    if current_user.role != UserRole.CAREGIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Caregiver access required",
        )
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency that ensures the current user is an admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )
    return current_user


async def get_patient_profile(
    current_user: User = Depends(require_patient),
    db: AsyncSession = Depends(get_db),
) -> PatientProfile:
    """Get the patient profile for the current authenticated patient."""
    result = await db.execute(
        select(PatientProfile).where(PatientProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found",
        )
    return profile


async def get_caregiver_profile(
    current_user: User = Depends(require_caregiver),
    db: AsyncSession = Depends(get_db),
) -> CaregiverProfile:
    """Get the caregiver profile for the current authenticated caregiver."""
    result = await db.execute(
        select(CaregiverProfile).where(CaregiverProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver profile not found",
        )
    return profile


async def verify_caregiver_patient_access(
    caregiver_profile_id: UUID,
    patient_profile_id: UUID,
    db: AsyncSession,
) -> bool:
    """
    Verify that a caregiver has an active link to a specific patient.
    A caregiver cannot access a patient they are not linked to.
    """
    result = await db.execute(
        select(PatientCaregiverLink).where(
            PatientCaregiverLink.caregiver_profile_id == caregiver_profile_id,
            PatientCaregiverLink.patient_profile_id == patient_profile_id,
            PatientCaregiverLink.status == LinkStatus.ACTIVE,
        )
    )
    link = result.scalar_one_or_none()
    if link is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this patient's data",
        )
    return True

"""
SmritiSaathi — Auth API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import (
    PatientRegisterRequest,
    CaregiverRegisterRequest,
    LoginRequest,
    TokenResponse,
    UserInfo,
)
from app.services import auth_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/patient", response_model=TokenResponse)
async def register_patient(
    data: PatientRegisterRequest, db: AsyncSession = Depends(get_db)
):
    """Register a new patient and return an access token."""
    try:
        return await auth_service.register_patient(data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register/caregiver", response_model=TokenResponse)
async def register_caregiver(
    data: CaregiverRegisterRequest, db: AsyncSession = Depends(get_db)
):
    """Register a new caregiver and return an access token."""
    try:
        return await auth_service.register_caregiver(data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate a user and return an access token."""
    try:
        return await auth_service.login_user(data.email, data.password, db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserInfo)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return current_user

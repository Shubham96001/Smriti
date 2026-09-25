"""
SmritiSaathi — Assessment Routes

Handles a patient's one-time Baseline RUDAS assessment and the subsequent fetch flow.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_patient
from app.core.database import get_db
from app.models.patient import PatientProfile
from app.schemas.assessment import RudasAssessmentSubmit, RudasAssessmentOut
from app.services.assessment_service import submit_assessment, get_assessment

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("/baseline", response_model=RudasAssessmentOut)
async def submit_baseline_assessment(
    data: RudasAssessmentSubmit,
    current_user=Depends(require_patient),
    db: AsyncSession = Depends(get_db),
):
    """Record a patient baseline assessment and mark their baseline as completed."""
    result = await db.execute(
        select(PatientProfile).where(PatientProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found",
        )

    if profile.baseline_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Baseline assessment has already been completed",
        )

    assessment = await submit_assessment(profile.id, data, db)
    return RudasAssessmentOut.model_validate(assessment)


@router.get("/baseline", response_model=RudasAssessmentOut | None)
async def get_baseline_assessment(
    current_user=Depends(require_patient),
    db: AsyncSession = Depends(get_db),
):
    """Return the most recent completed baseline assessment for the patient."""
    result = await db.execute(
        select(PatientProfile).where(PatientProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found",
        )

    assessment = await get_assessment(profile.id, db)
    if assessment is None:
        return None

    return RudasAssessmentOut.model_validate(assessment)

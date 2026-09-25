"""
SmritiSaathi — Assessment Service

Handles RUDAS baseline assessment creation, response saving, and scoring.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessment import RudasAssessment, RudasResponse
from app.models.patient import PatientProfile
from app.schemas.assessment import RudasAssessmentSubmit, RudasAssessmentOut


async def get_or_create_assessment(
    patient_profile_id: UUID, db: AsyncSession
) -> RudasAssessment:
    """
    Get existing incomplete assessment or create a new one.
    Prevents duplicate assessments.
    """
    # Check for existing incomplete assessment
    result = await db.execute(
        select(RudasAssessment).where(
            RudasAssessment.patient_profile_id == patient_profile_id,
            RudasAssessment.is_completed == False,
        )
    )
    assessment = result.scalar_one_or_none()

    if assessment:
        return assessment

    # Check if baseline already completed
    completed_result = await db.execute(
        select(RudasAssessment).where(
            RudasAssessment.patient_profile_id == patient_profile_id,
            RudasAssessment.is_completed == True,
        )
    )
    if completed_result.scalar_one_or_none():
        raise ValueError("Baseline assessment already completed")

    # Create new assessment
    assessment = RudasAssessment(
        patient_profile_id=patient_profile_id,
        is_completed=False,
    )
    db.add(assessment)
    await db.flush()
    return assessment


async def submit_assessment(
    patient_profile_id: UUID,
    data: RudasAssessmentSubmit,
    db: AsyncSession,
) -> RudasAssessment:
    """
    Submit and score a complete RUDAS assessment.
    1. Get or create assessment record
    2. Save all domain responses
    3. Calculate total score
    4. Mark as completed
    5. Update patient profile baseline_completed flag
    """
    assessment = await get_or_create_assessment(patient_profile_id, db)

    # Clear any existing responses (in case of re-submission of incomplete)
    await db.execute(
        RudasResponse.__table__.delete().where(
            RudasResponse.assessment_id == assessment.id
        )
    )

    # Save individual responses
    total_score = 0.0
    for resp in data.responses:
        response = RudasResponse(
            assessment_id=assessment.id,
            domain=resp.domain,
            question_number=resp.question_number,
            response_value=resp.response_value,
            score=resp.score,
            max_score=resp.max_score,
            notes=resp.notes,
        )
        db.add(response)
        total_score += resp.score

    # Update assessment
    assessment.total_score = total_score
    assessment.is_completed = True

    # Mark patient baseline as completed
    result = await db.execute(
        select(PatientProfile).where(PatientProfile.id == patient_profile_id)
    )
    patient = result.scalar_one_or_none()
    if patient:
        patient.baseline_completed = True

    await db.flush()
    return assessment


async def get_assessment(
    patient_profile_id: UUID, db: AsyncSession
) -> Optional[RudasAssessment]:
    """Get the completed baseline assessment for a patient."""
    result = await db.execute(
        select(RudasAssessment)
        .where(
            RudasAssessment.patient_profile_id == patient_profile_id,
            RudasAssessment.is_completed == True,
        )
        .order_by(RudasAssessment.assessment_date.desc())
    )
    return result.scalar_one_or_none()

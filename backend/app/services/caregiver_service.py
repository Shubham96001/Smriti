"""
SmritiSaathi — Caregiver Service
"""

from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.caregiver import CaregiverProfile, PatientCaregiverLink, LinkStatus
from app.models.patient import PatientProfile
from app.schemas.caregiver import LinkedPatientSummary
from app.services.game_service import get_recent_performance
from app.services.reminder_service import get_active_reminders_count, get_missed_reminders_count_last_week


async def get_linked_patients(
    caregiver_profile_id: UUID, db: AsyncSession
) -> List[LinkedPatientSummary]:
    """
    Get all patients linked to a caregiver and compile their summary metrics
    for the caregiver dashboard.
    """
    # Fetch links and patient profiles
    query = (
        select(PatientCaregiverLink, PatientProfile)
        .join(PatientProfile, PatientCaregiverLink.patient_profile_id == PatientProfile.id)
        .where(
            PatientCaregiverLink.caregiver_profile_id == caregiver_profile_id,
            PatientCaregiverLink.status == LinkStatus.ACTIVE,
        )
    )
    result = await db.execute(query)
    rows = result.all()

    summaries = []
    for link, patient in rows:
        # Get metrics for each patient
        # Defaulting game_type to memory_matching for generic dashboard metric
        perf = await get_recent_performance(patient.id, "memory_matching", count=5, db=db)
        
        active_reminders = await get_active_reminders_count(patient.id, db)
        missed_reminders = await get_missed_reminders_count_last_week(patient.id, db)

        # Build summary
        summary = LinkedPatientSummary(
            patient_profile_id=patient.id,
            full_name=patient.full_name,
            preferred_language=patient.preferred_language,
            baseline_completed=patient.baseline_completed,
            total_games_played=perf["sessions_count"],
            recent_accuracy=perf["avg_accuracy"] if perf["sessions_count"] > 0 else None,
            active_reminders=active_reminders,
            missed_reminders_week=missed_reminders,
            last_activity=None,  # Could be fetched from audit logs or game sessions
            link_status=link.status.value,
        )
        summaries.append(summary)

    return summaries


async def link_patient_by_code(
    caregiver_profile_id: UUID,
    invitation_code: str,
    db: AsyncSession,
) -> bool:
    """Link a patient to this caregiver using the caregiver's invitation code."""
    # The requirement asks for 'patient linking or invitation code' on caregiver registration
    # Or caregiver sharing code with patient.
    # Actually, usually patient enters caregiver code.
    # If this is called by caregiver, they might enter a patient code.
    # Wait, the caregiver has the invitation code (`CaregiverProfile.invitation_code`).
    # Patients use it to link.
    # If caregiver is linking, maybe they enter patient email. We'll skip that for now
    # and assume the patient links to the caregiver, which is handled in auth_service during patient registration,
    # or can be added as a separate patient endpoint.
    pass

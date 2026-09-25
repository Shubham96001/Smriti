"""
SmritiSaathi — Models Package

Imports all models so SQLAlchemy metadata is complete.
This module must be imported before running migrations or creating tables.
"""

from app.models.user import User, UserRole
from app.models.patient import PatientProfile
from app.models.caregiver import CaregiverProfile, PatientCaregiverLink, LinkStatus
from app.models.assessment import RudasAssessment, RudasResponse
from app.models.game import GameSession, GameEvent, DifficultyDecision
from app.models.memory import MemoryItem
from app.models.reminder import Reminder, ReminderEvent, ReminderType, Recurrence, ReminderEventStatus
from app.models.audit import AuditLog, CaregiverAlert

__all__ = [
    "User", "UserRole",
    "PatientProfile",
    "CaregiverProfile", "PatientCaregiverLink", "LinkStatus",
    "RudasAssessment", "RudasResponse",
    "GameSession", "GameEvent", "DifficultyDecision",
    "MemoryItem",
    "Reminder", "ReminderEvent", "ReminderType", "Recurrence", "ReminderEventStatus",
    "AuditLog", "CaregiverAlert",
]

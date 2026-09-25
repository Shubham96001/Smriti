"""
SmritiSaathi — Game Service

Handles game session lifecycle and performance tracking.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import GameSession, GameEvent
from app.schemas.game import StartGameRequest, EndGameRequest, GameSessionOut


async def start_game_session(
    patient_profile_id: UUID,
    data: StartGameRequest,
    difficulty_override: Optional[int],
    db: AsyncSession,
) -> GameSession:
    """Create a new game session."""
    session = GameSession(
        patient_profile_id=patient_profile_id,
        game_type=data.game_type,
        difficulty_level=difficulty_override or data.difficulty_level or 1,
    )
    db.add(session)
    await db.flush()
    return session


async def end_game_session(
    session_id: UUID,
    patient_profile_id: UUID,
    data: EndGameRequest,
    db: AsyncSession,
) -> GameSession:
    """
    Complete a game session:
    1. Update aggregate metrics
    2. Save individual events
    3. Mark as completed
    """
    result = await db.execute(
        select(GameSession).where(
            GameSession.id == session_id,
            GameSession.patient_profile_id == patient_profile_id,
        )
    )
    session = result.scalar_one_or_none()
    if session is None:
        raise ValueError("Game session not found")

    if session.is_completed:
        raise ValueError("Game session already completed")

    # Update session metrics
    session.total_score = data.total_score
    session.max_score = data.max_score
    session.accuracy = data.accuracy
    session.avg_response_time_ms = data.avg_response_time_ms
    session.hints_used = data.hints_used
    session.is_completed = True
    session.ended_at = datetime.now(timezone.utc)

    # Save events
    for event_data in data.events:
        event = GameEvent(
            session_id=session.id,
            event_type=event_data.event_type,
            event_data=event_data.event_data,
            response_time_ms=event_data.response_time_ms,
            is_correct=event_data.is_correct,
        )
        db.add(event)

    await db.flush()
    return session


async def get_game_history(
    patient_profile_id: UUID,
    game_type: Optional[str],
    limit: int,
    db: AsyncSession,
) -> List[GameSession]:
    """Get game session history for a patient."""
    query = select(GameSession).where(
        GameSession.patient_profile_id == patient_profile_id,
        GameSession.is_completed == True,
    )
    if game_type:
        query = query.where(GameSession.game_type == game_type)
    query = query.order_by(GameSession.ended_at.desc()).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_recent_performance(
    patient_profile_id: UUID,
    game_type: str,
    count: int,
    db: AsyncSession,
) -> dict:
    """Get recent performance metrics for adaptive difficulty calculations."""
    sessions = await get_game_history(patient_profile_id, game_type, count, db)

    if not sessions:
        return {
            "sessions_count": 0,
            "avg_accuracy": 0.0,
            "avg_response_time_ms": 0,
            "avg_hints_used": 0.0,
            "last_difficulty": 1,
            "trend": "neutral",
        }

    accuracies = [s.accuracy for s in sessions]
    response_times = [s.avg_response_time_ms for s in sessions if s.avg_response_time_ms]
    hints = [s.hints_used for s in sessions]

    avg_accuracy = sum(accuracies) / len(accuracies)

    # Determine trend from recent sessions
    if len(accuracies) >= 3:
        recent_avg = sum(accuracies[:3]) / 3
        older_avg = sum(accuracies[3:]) / max(len(accuracies[3:]), 1) if len(accuracies) > 3 else recent_avg
        if recent_avg > older_avg + 0.1:
            trend = "improving"
        elif recent_avg < older_avg - 0.1:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "neutral"

    return {
        "sessions_count": len(sessions),
        "avg_accuracy": avg_accuracy,
        "avg_response_time_ms": sum(response_times) // max(len(response_times), 1) if response_times else 0,
        "avg_hints_used": sum(hints) / max(len(hints), 1),
        "last_difficulty": sessions[0].difficulty_level,
        "trend": trend,
    }

"""
SmritiSaathi — Adaptive Difficulty Service

Rule-based adaptive engine that adjusts game difficulty based on performance.
Saves every decision with its rationale for review and improvement.

This is the initial reliable, explainable engine.
An advanced ML model can be added after the basic system works correctly.
"""

from typing import Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import DifficultyDecision
from app.services.game_service import get_recent_performance


# Game-specific difficulty parameters
DIFFICULTY_PARAMS = {
    "memory_matching": {
        1: {"pairs": 3, "time_limit_sec": 120, "hints_available": 3},
        2: {"pairs": 4, "time_limit_sec": 100, "hints_available": 2},
        3: {"pairs": 5, "time_limit_sec": 90, "hints_available": 2},
        4: {"pairs": 6, "time_limit_sec": 80, "hints_available": 1},
        5: {"pairs": 8, "time_limit_sec": 70, "hints_available": 1},
    },
    "pattern_sequence": {
        1: {"sequence_length": 3, "options": 3, "time_limit_sec": 30, "hints_available": 3},
        2: {"sequence_length": 4, "options": 4, "time_limit_sec": 25, "hints_available": 2},
        3: {"sequence_length": 5, "options": 4, "time_limit_sec": 20, "hints_available": 2},
        4: {"sequence_length": 5, "options": 5, "time_limit_sec": 18, "hints_available": 1},
        5: {"sequence_length": 6, "options": 6, "time_limit_sec": 15, "hints_available": 1},
    },
    "attention": {
        1: {"targets": 3, "distractors": 2, "time_limit_sec": 30, "hints_available": 3},
        2: {"targets": 3, "distractors": 4, "time_limit_sec": 25, "hints_available": 2},
        3: {"targets": 4, "distractors": 5, "time_limit_sec": 22, "hints_available": 2},
        4: {"targets": 4, "distractors": 6, "time_limit_sec": 20, "hints_available": 1},
        5: {"targets": 5, "distractors": 8, "time_limit_sec": 18, "hints_available": 1},
    },
    "daily_routine": {
        1: {"items": 3, "categories": 1, "time_limit_sec": 60, "hints_available": 3},
        2: {"items": 4, "categories": 2, "time_limit_sec": 50, "hints_available": 2},
        3: {"items": 5, "categories": 2, "time_limit_sec": 45, "hints_available": 2},
        4: {"items": 6, "categories": 3, "time_limit_sec": 40, "hints_available": 1},
        5: {"items": 7, "categories": 3, "time_limit_sec": 35, "hints_available": 1},
    },
}


async def get_recommended_difficulty(
    patient_profile_id: UUID,
    game_type: str,
    db: AsyncSession,
) -> Dict[str, Any]:
    """
    Calculate recommended difficulty for the next game session.

    Logic:
    - If accuracy high (>= 0.8) and stable response time: increase difficulty
    - If accuracy moderate (0.5-0.8): maintain difficulty
    - If accuracy low (< 0.5) or excessive hints: decrease difficulty
    - Never go below 1 or above 5
    - For new players: start at 1
    """
    performance = await get_recent_performance(
        patient_profile_id, game_type, count=5, db=db
    )

    current_difficulty = performance["last_difficulty"]
    avg_accuracy = performance["avg_accuracy"]
    avg_hints = performance["avg_hints_used"]
    sessions_count = performance["sessions_count"]
    trend = performance["trend"]

    # New player — start at level 1
    if sessions_count == 0:
        reason = "First time playing this game — starting at beginner level"
        new_difficulty = 1
    # High accuracy, low hints, stable or improving
    elif avg_accuracy >= 0.8 and avg_hints <= 1.0 and trend in ("improving", "stable", "neutral"):
        new_difficulty = min(current_difficulty + 1, 5)
        reason = f"Good performance (accuracy: {avg_accuracy:.0%}, hints: {avg_hints:.1f}) — increasing difficulty"
    # Low accuracy or too many hints
    elif avg_accuracy < 0.5 or avg_hints >= 2.5:
        new_difficulty = max(current_difficulty - 1, 1)
        reason = f"Needs more support (accuracy: {avg_accuracy:.0%}, hints: {avg_hints:.1f}) — simplifying task"
    # Declining performance
    elif trend == "declining" and avg_accuracy < 0.65:
        new_difficulty = max(current_difficulty - 1, 1)
        reason = f"Performance variation observed (accuracy: {avg_accuracy:.0%}, trend: declining) — adjusting difficulty"
    # Moderate performance — maintain
    else:
        new_difficulty = current_difficulty
        reason = f"Steady performance (accuracy: {avg_accuracy:.0%}) — maintaining current level"

    # Save the decision
    decision = DifficultyDecision(
        patient_profile_id=patient_profile_id,
        game_type=game_type,
        previous_difficulty=current_difficulty,
        new_difficulty=new_difficulty,
        reason=reason,
        metrics_snapshot=performance,
    )
    db.add(decision)
    await db.flush()

    # Get difficulty parameters
    params = DIFFICULTY_PARAMS.get(game_type, {}).get(new_difficulty, {})

    return {
        "game_type": game_type,
        "recommended_difficulty": new_difficulty,
        "reason": reason,
        "parameters": params,
    }

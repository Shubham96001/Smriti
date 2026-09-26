from statistics import mean
from typing import Any


def choose_difficulty(
    current_level: int,
    accuracies: list[float],
    hints_used: list[int],
) -> dict[str, Any]:
    """Pure, conservative adaptive rule: downgrades need less evidence than upgrades."""
    level = max(1, min(5, current_level))
    accuracy = mean(accuracies) if accuracies else None
    hints = mean(hints_used) if hints_used else None
    change = 0
    reason = "Insufficient evidence; keeping current level"
    if len(accuracies) >= 2 and accuracy is not None and (accuracy < 0.5 or (hints is not None and hints >= 3)):
        change = -1
        reason = "Recent play suggests a simpler level may be more comfortable"
    elif len(accuracies) >= 4 and accuracy is not None and accuracy >= 0.85 and (hints is None or hints <= 1):
        change = 1
        reason = "Consistent recent play supports a small increase"
    next_level = max(1, min(5, level + change))
    return {
        "level": next_level,
        "reason": reason if next_level != level else ("Already at the supported level boundary" if change else reason),
        "metrics": {"accuracy_mean": accuracy, "hints_mean": hints, "evidence_count": len(accuracies)},
    }
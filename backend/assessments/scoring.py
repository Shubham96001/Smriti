def calculate_placeholder_score(scores: list[int | None]) -> int | None:
    """Aggregate development-only values; this is not clinical scoring."""
    answered = [score for score in scores if score is not None]
    return sum(answered) if answered else None
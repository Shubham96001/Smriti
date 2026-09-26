from backend.ai.adaptive_engine import choose_difficulty


def test_first_evidence_keeps_level():
    assert choose_difficulty(2, [1.0], [0])["level"] == 2


def test_hard_performance_downgrades_one_level():
    assert choose_difficulty(4, [0.2, 0.4], [2, 3])["level"] == 3


def test_upgrade_requires_more_evidence_and_changes_one_level():
    assert choose_difficulty(2, [1.0] * 3, [0] * 3)["level"] == 2
    assert choose_difficulty(2, [1.0] * 4, [0] * 4)["level"] == 3


def test_difficulty_is_clamped():
    assert choose_difficulty(5, [1.0] * 4, [0] * 4)["level"] == 5
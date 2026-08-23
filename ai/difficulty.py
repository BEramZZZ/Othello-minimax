from ai.evaluation import piece_count_eval, strategic_eval

DIFFICULTIES = {
    "easy":   {"depth": 2, "eval_fn": piece_count_eval},
    "medium": {"depth": 4, "eval_fn": piece_count_eval},
    "hard":   {"depth": 6, "eval_fn": strategic_eval},
}


def settings_for(difficulty):
    """Return {"depth": int, "eval_fn": callable} for a difficulty name. Raises if unknown."""
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"Unknown difficulty: {difficulty!r}")
    return DIFFICULTIES[difficulty]
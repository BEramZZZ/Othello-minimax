"""
difficulty.py

Maps a difficulty name to a search depth AND an evaluation function.
Easy/medium stay on the weak piece_count_eval (matches their shallow
search -- no point pairing a strong heuristic with a search too shallow
to exploit it). Hard switches to strategic_eval, where the deeper search
actually has room to act on corners/mobility/stability.
"""

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
import json
import os

SAVE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saves", "othello_save.json"
)


def save_game(state, choice):
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    data = {"grid": state.board.grid, "current_player": state.current_player, "choice": choice}
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f)


def load_game():
    """Returns (GameState, choice), or None if there's no save / it's unreadable."""
    if not os.path.exists(SAVE_PATH):
        return None
    try:
        with open(SAVE_PATH) as f:
            data = json.load(f)
        from game.game_state import GameState
        state = GameState.from_dict({"grid": data["grid"], "current_player": data["current_player"]})
        return state, data["choice"]
    except (json.JSONDecodeError, KeyError, OSError):
        return None


def save_exists():
    return os.path.exists(SAVE_PATH)


def delete_save():
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)
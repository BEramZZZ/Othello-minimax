# Othello (Reversi)

Python + Pygame implementation of Othello, with two game modes, a 3-level
minimax AI, save/load, undo, and a full menu system that never requires
closing the window to restart or change modes.

## Features

- **Human vs Human** and **Human vs AI** game modes.
- **3 AI difficulties** (Easy / Medium / Hard), each mapped to a search
  depth and an evaluation function:
  - Easy — depth 2, disc-count evaluation
  - Medium — depth 4, disc-count evaluation
  - Hard — depth 6, strategic evaluation (corners + mobility + stability)
- **Minimax with alpha-beta pruning** and move ordering
  (corners tried first, X-squares last) for fast search even at depth 6.
- **Undo** — reverts a full human-move-then-AI-reply pair in one click.
- **Save / Continue** — single-slot save to disk; resume a game after
  fully closing and reopening the app.
- **Per-turn timer** and a pass banner shown in the GUI (not just console).
- **Menu / restart loop** — change mode, replay, or return to the menu
  without relaunching the app.
- Styled UI: gradient board with a wooden border, discs with shadow/highlight,
  a top bar with turn indicator and timer, a restyled menu.

## Project structure

```
othello/
├── main.py                  # Entry point: menu -> session loop -> game loop
├── config.py                 # Constants: layout, colors, fonts, window size
├── game/
│   ├── __init__.py
│   ├── board.py               # Board state, legal moves, flipping, clone()
│   ├── game_state.py           # Turn management, pass handling, undo, win/draw
│   ├── player.py                # HumanPlayer / AIPlayer
│   └── save_load.py              # Single-slot JSON save/load
├── ai/
│   ├── __init__.py
│   ├── minimax.py               # Minimax + alpha-beta + move ordering
│   ├── evaluation.py             # piece_count_eval, strategic_eval
│   └── difficulty.py              # easy/medium/hard -> (depth, eval_fn)
├── gui/
│   ├── __init__.py
│   ├── renderer.py               # Board, pieces, top bar, banners, game-over
│   ├── event_handler.py           # Pixel -> board cell
│   ├── menu.py                     # Mode/difficulty/continue selection screens
│   └── ui_helpers.py                # Shared Button + gradient drawing
├── saves/
│   └── othello_save.json           # Created at runtime by Save
└── README.md
```

## Requirements

- Python 3.10+
- Pygame (`pip install pygame`)

## How to run

From the project root:

```
python main.py
```

`main.py` sits at the project root, so it can be run directly — no `-m`
flag needed (that's only required when running a file that lives inside
a subfolder like `game/` or `ai/` on its own, e.g. while testing a single
module in isolation).

## How to play

1. On launch, choose a game mode: **Human vs Human**, **Human vs AI**, or
   **Continue Saved Game** (only shown if a save exists).
2. For Human vs AI, pick a difficulty: **Easy**, **Medium**, or **Hard**.
3. Click a highlighted square to play there. Legal moves are marked with
   a small dot.
4. If a player has no legal moves, their turn is skipped automatically
   and a banner announces the pass.
5. In-game buttons (top right): **Undo**, **Save**, **Menu**.
6. On game over: **Play Again** (same mode/difficulty) or **Main Menu**.

## Architecture notes

Three independent layers, kept deliberately decoupled:

- **`game/`** — pure rules and state. No Pygame import anywhere in this
  folder; the whole engine (including the AI) can be run and tested from
  the terminal with zero GUI code involved.
- **`ai/`** — minimax search and evaluation. Depends only on `game/`.
- **`gui/`** — rendering and input handling. Talks to `game/` and `ai/`
  only through `game/player.py`'s `HumanPlayer` / `AIPlayer` interface.

`main.py` is the only file that ties all three layers together, via a
three-level control flow:

```
main()                     outer loop: shows the menu, dispatches to play_session
  -> play_session()          inner loop: replays the SAME mode/difficulty
                              while the player clicks "Play Again"
    -> _run_single_game()      one full game; returns "menu" / "restart" / "quit"
```

## Known limitations

- No automated test suite (`tests/` was scoped in the original build plan
  but skipped by choice).
- Save is single-slot — saving overwrites any existing save.
- Human is always Black in Human vs AI mode; no color selection.

## Author

BELAIDI Ramzy Zakaria — Master's student, USTHB (AI / Bioinformatics / CS)

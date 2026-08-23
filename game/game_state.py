"""
game_state.py

Step 12 additions on top of steps 1-10's turn/pass/game-over logic:
  - Move history: a stack of (grid_before, player_before) snapshots,
    pushed before every move or pass, so undo() can restore either.
  - undo(): pops the most recent snapshot. One call = one ply reverted.
  - to_dict()/from_dict(): plain-data form for JSON save/load. History is
    NOT included -- a loaded game starts with a clean undo stack, since
    there's nothing before the save point to go back to.
"""

import copy

from .board import Board, BLACK, WHITE, SYMBOLS


class GameState:
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK
        self._history = []

    def legal_moves(self):
        return self.board.legal_moves(self.current_player)

    def is_game_over(self):
        black_has_move = bool(self.board.legal_moves(BLACK))
        white_has_move = bool(self.board.legal_moves(WHITE))
        return not black_has_move and not white_has_move

    def _snapshot(self):
        self._history.append((copy.deepcopy(self.board.grid), self.current_player))

    def play_move(self, row, col):
        self._snapshot()
        self.board.apply_move(row, col, self.current_player)
        self._advance_turn()

    def pass_turn(self):
        self._snapshot()
        self._advance_turn()

    def _advance_turn(self):
        self.current_player = self.board.opponent(self.current_player)

    def can_undo(self):
        return len(self._history) > 0

    def undo(self):
        """Revert exactly one ply (a move or a pass). Returns True if
        something was undone, False if the history was already empty."""
        if not self._history:
            return False
        grid, player = self._history.pop()
        self.board.grid = grid
        self.current_player = player
        return True

    def winner(self):
        black, white = self.board.count()
        if black > white:
            return BLACK
        if white > black:
            return WHITE
        return None

    def to_dict(self):
        return {"grid": self.board.grid, "current_player": self.current_player}

    @classmethod
    def from_dict(cls, data):
        state = cls()
        state.board.grid = data["grid"]
        state.current_player = data["current_player"]
        return state


def _prompt_move():
    raw = input("Enter your move as row,col (e.g. 2,3): ").strip()
    row_str, col_str = raw.split(",")
    return int(row_str), int(col_str)


def play_console_game():
    state = GameState()
    while not state.is_game_over():
        print()
        print(state.board)
        moves = state.legal_moves()
        player_symbol = SYMBOLS[state.current_player]

        if not moves:
            print(f"\n{player_symbol} has no legal moves -- passing.")
            state.pass_turn()
            continue

        print(f"\n{player_symbol} to move. Legal moves: {moves}")
        while True:
            try:
                row, col = _prompt_move()
            except ValueError:
                print("Please enter it as row,col -- e.g. 2,3")
                continue
            if (row, col) in moves:
                break
            print("That's not a legal move. Try again.")

        state.play_move(row, col)

    print()
    print(state.board)
    black, white = state.board.count()
    print(f"\nGame over. Black: {black}, White: {white}")
    winner = state.winner()
    print("It's a draw." if winner is None else f"{SYMBOLS[winner]} wins!")


if __name__ == "__main__":
    play_console_game()
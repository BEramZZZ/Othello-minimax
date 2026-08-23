"""
game_state.py

Turn management, passing, and game-over detection, plus a console-playable
human vs human loop. Still no Pygame, no AI -- this is the last thing we
verify from the terminal before any graphics exist.

Run it with:  python -m game.game_state   (from the project root)
"""

from .board import Board, BLACK, WHITE, SYMBOLS


class GameState:
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK  # Black moves first in Othello

    def legal_moves(self):
        return self.board.legal_moves(self.current_player)

    def is_game_over(self):
        """
        The game ends when NEITHER player has a legal move -- not just
        when the current player is stuck (that only triggers a pass).
        """
        black_has_move = bool(self.board.legal_moves(BLACK))
        white_has_move = bool(self.board.legal_moves(WHITE))
        return not black_has_move and not white_has_move

    def play_move(self, row, col):
        """Apply a move for the current player, then hand the turn over."""
        self.board.apply_move(row, col, self.current_player)
        self._advance_turn()

    def pass_turn(self):
        """Current player has no legal moves; turn passes without playing."""
        self._advance_turn()

    def _advance_turn(self):
        self.current_player = self.board.opponent(self.current_player)

    def winner(self):
        """Return BLACK, WHITE, or None for a draw. Only meaningful once the game is over."""
        black, white = self.board.count()
        if black > white:
            return BLACK
        if white > black:
            return WHITE
        return None


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
    if winner is None:
        print("It's a draw.")
    else:
        print(f"{SYMBOLS[winner]} wins!")


if __name__ == "__main__":
    play_console_game()
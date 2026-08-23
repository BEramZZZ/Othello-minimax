"""
board.py

Board representation and rules for Othello (Reversi).
No Pygame, no AI code here on purpose: this module has to work standalone
from the terminal so we can test and trust it before any GUI or AI exists.
"""

BOARD_SIZE = 8

EMPTY = 0
BLACK = 1
WHITE = 2

# All 8 directions a line of flipped discs can run in: (row_delta, col_delta)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]

SYMBOLS = {EMPTY: ".", BLACK: "B", WHITE: "W"}


class Board:
    def __init__(self):
        # 8x8 grid, row-major: self.grid[row][col]
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Standard Othello starting position (0-indexed)
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE

    def opponent(self, player):
        return BLACK if player == WHITE else WHITE

    def in_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def _flips_in_direction(self, row, col, player, dr, dc):
        """
        Walk one direction from (row, col). Return the list of opponent
        coordinates that would be flipped if `player` played at (row, col)
        in this direction. Empty list means this direction flips nothing.
        """
        opp = self.opponent(player)
        r, c = row + dr, col + dc
        line = []

        while self.in_bounds(r, c) and self.grid[r][c] == opp:
            line.append((r, c))
            r += dr
            c += dc

        # A valid flip line must be non-empty and end on player's own disc
        if line and self.in_bounds(r, c) and self.grid[r][c] == player:
            return line
        return []

    def legal_moves(self, player):
        """
        Return every (row, col) where `player` can legally place a disc,
        i.e. it flips at least one opponent disc in at least one direction.
        """
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] != EMPTY:
                    continue
                for dr, dc in DIRECTIONS:
                    if self._flips_in_direction(row, col, player, dr, dc):
                        moves.append((row, col))
                        break  # one valid direction is enough
        return moves

    def apply_move(self, row, col, player):
        """
        Place `player`'s disc at (row, col) and flip every disc it captures.
        Assumes (row, col) is legal — check with legal_moves() first.
        Returns the list of flipped coordinates (useful later for GUI animation).
        """
        flips = []
        for dr, dc in DIRECTIONS:
            flips.extend(self._flips_in_direction(row, col, player, dr, dc))

        self.grid[row][col] = player
        for r, c in flips:
            self.grid[r][c] = player

        return flips

    def count(self):
        """Return (black_count, white_count)."""
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white

    def __str__(self):
        header = "  " + " ".join(str(c) for c in range(BOARD_SIZE))
        lines = [header]
        for r in range(BOARD_SIZE):
            row_str = " ".join(SYMBOLS[cell] for cell in self.grid[r])
            lines.append(f"{r} {row_str}")
        return "\n".join(lines)


if __name__ == "__main__":
    board = Board()
    print("Starting position:")
    print(board)
    print()

    black_moves = board.legal_moves(BLACK)
    print(f"Black's legal opening moves: {black_moves}")

    move = black_moves[0]
    print(f"\nBlack plays {move}")
    flipped = board.apply_move(move[0], move[1], BLACK)
    print(f"Flipped: {flipped}")
    print(board)

    white_moves = board.legal_moves(WHITE)
    print(f"\nWhite's legal moves now: {white_moves}")

    black, white = board.count()
    print(f"\nScore -- Black: {black}, White: {white}")
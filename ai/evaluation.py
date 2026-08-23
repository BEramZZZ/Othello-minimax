from game.board import BOARD_SIZE, EMPTY, BLACK, WHITE

CORNERS = [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]

# Squares diagonally adjacent to each corner -- playing here (before you
# own the corner) usually just hands the corner to your opponent.
X_SQUARES = [(1, 1), (1, BOARD_SIZE - 2), (BOARD_SIZE - 2, 1), (BOARD_SIZE - 2, BOARD_SIZE - 2)]

# Weights: corners dominate, mobility and stability matter, raw disc
# count barely does until the board fills up.
WEIGHT_CORNERS = 25
WEIGHT_MOBILITY = 5
WEIGHT_STABILITY = 3
WEIGHT_DISCS = 1


def piece_count_eval(board, player):
    """Kept from step 5: pure disc-count difference, scored for `player`."""
    black, white = board.count()
    player_count = black if player == BLACK else white
    opponent_count = white if player == BLACK else black
    return player_count - opponent_count


def _opponent(player):
    return BLACK if player == WHITE else WHITE


def _corner_score(board, player, opponent):
    """+1 per corner player owns, -1 per corner opponent owns."""
    score = 0
    for row, col in CORNERS:
        occupant = board.grid[row][col]
        if occupant == player:
            score += 1
        elif occupant == opponent:
            score -= 1
    return score


def _mobility_score(board, player, opponent):
    """
    Difference in legal-move counts. Normalized-ish by just taking the raw
    difference -- good enough at these weights, no need for percentages.
    """
    player_moves = len(board.legal_moves(player))
    opponent_moves = len(board.legal_moves(opponent))
    return player_moves - opponent_moves


def _stability_score(board, player, opponent):
    """
    Rough stability proxy: for each corner YOU own, the two squares
    orthogonally adjacent to it (along the edges) are effectively locked in
    too, since flipping them would require flipping through your corner
    disc, which is impossible. This undercounts real stability (doesn't
    chase stable lines further along the edge) but avoids a much heavier
    full stability search, and is a solid improvement over ignoring it.
    """
    score = 0
    for corner_row, corner_col in CORNERS:
        occupant = board.grid[corner_row][corner_col]
        if occupant not in (player, opponent):
            continue

        # The two edge-adjacent squares next to this corner (not diagonal).
        adj = []
        row_dir = 1 if corner_row == 0 else -1
        col_dir = 1 if corner_col == 0 else -1
        adj.append((corner_row + row_dir, corner_col))
        adj.append((corner_row, corner_col + col_dir))

        for r, c in adj:
            if board.grid[r][c] == occupant:
                score += 1 if occupant == player else -1
    return score


def strategic_eval(board, player):
    """
    Combined weighted heuristic from `player`'s perspective. Positive
    favors `player`, negative favors the opponent.
    """
    opponent = _opponent(player)

    corners = _corner_score(board, player, opponent)
    mobility = _mobility_score(board, player, opponent)
    stability = _stability_score(board, player, opponent)
    discs = piece_count_eval(board, player)

    return (
        WEIGHT_CORNERS * corners
        + WEIGHT_MOBILITY * mobility
        + WEIGHT_STABILITY * stability
        + WEIGHT_DISCS * discs
    )
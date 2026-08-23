from game.board import BLACK, WHITE, BOARD_SIZE

CORNERS = {(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)}
X_SQUARES = {(1, 1), (1, BOARD_SIZE - 2), (BOARD_SIZE - 2, 1), (BOARD_SIZE - 2, BOARD_SIZE - 2)}


def _opponent(player):
    return BLACK if player == WHITE else WHITE


def _move_priority(move):
    if move in CORNERS:
        return 0
    if move in X_SQUARES:
        return 2
    return 1


def _ordered(moves):
    """Sort legal moves corners-first, X-squares-last. Stable sort keeps
    the original relative order within each priority tier."""
    return sorted(moves, key=_move_priority)


def minimax(board, depth, current_player, root_player, eval_fn, alpha=float("-inf"), beta=float("inf")):
    legal = board.legal_moves(current_player)

    if not legal:
        opponent = _opponent(current_player)
        if not board.legal_moves(opponent):
            return eval_fn(board, root_player)
        return minimax(board, depth, opponent, root_player, eval_fn, alpha, beta)

    if depth == 0:
        return eval_fn(board, root_player)

    ordered_moves = _ordered(legal)

    if current_player == root_player:
        best = float("-inf")
        for row, col in ordered_moves:
            child = board.clone()
            child.apply_move(row, col, current_player)
            score = minimax(child, depth - 1, _opponent(current_player), root_player, eval_fn, alpha, beta)
            best = max(best, score)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = float("inf")
        for row, col in ordered_moves:
            child = board.clone()
            child.apply_move(row, col, current_player)
            score = minimax(child, depth - 1, _opponent(current_player), root_player, eval_fn, alpha, beta)
            best = min(best, score)
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best


def find_best_move(board, player, depth, eval_fn):
    legal = board.legal_moves(player)
    if not legal:
        return None

    best_move = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for row, col in _ordered(legal):
        child = board.clone()
        child.apply_move(row, col, player)
        score = minimax(child, depth - 1, _opponent(player), player, eval_fn, alpha, beta)
        if score > best_score:
            best_score = score
            best_move = (row, col)
        alpha = max(alpha, best_score)

    return best_move
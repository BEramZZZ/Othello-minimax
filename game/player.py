"""
player.py

Step 9 change: AIPlayer now takes an eval_fn alongside depth, and passes
it through to find_best_move. Nothing else about this class changes.
"""

from ai.minimax import find_best_move
from ai.evaluation import piece_count_eval


class HumanPlayer:
    def __init__(self, color):
        self.color = color


class AIPlayer:
    def __init__(self, color, depth=3, eval_fn=piece_count_eval):
        self.color = color
        self.depth = depth
        self.eval_fn = eval_fn

    def get_move(self, board):
        return find_best_move(board, self.color, self.depth, self.eval_fn)
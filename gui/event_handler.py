"""
event_handler.py

Updated for the GUI overhaul: the board no longer starts at (MARGIN,
MARGIN) -- it starts below the top bar, at (BOARD_ORIGIN_X, BOARD_ORIGIN_Y).
"""

from config import BOARD_SIZE, CELL_SIZE, BOARD_ORIGIN_X, BOARD_ORIGIN_Y


def pixel_to_cell(pos):
    x, y = pos
    if x < BOARD_ORIGIN_X or y < BOARD_ORIGIN_Y:
        return None

    col = (x - BOARD_ORIGIN_X) // CELL_SIZE
    row = (y - BOARD_ORIGIN_Y) // CELL_SIZE

    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return int(row), int(col)
    return None
import pygame

from config import (
    BOARD_SIZE, CELL_SIZE, BOARD_ORIGIN_X, BOARD_ORIGIN_Y,
    WINDOW_WIDTH, WINDOW_HEIGHT, TOP_BAR_HEIGHT,
    COLOR_BOARD_TOP, COLOR_BOARD_BOTTOM, COLOR_BOARD_BORDER, COLOR_GRID_LINE,
    COLOR_BLACK_DISC_TOP, COLOR_BLACK_DISC_BOTTOM,
    COLOR_WHITE_DISC_TOP, COLOR_WHITE_DISC_BOTTOM,
    COLOR_ACCENT, COLOR_TEXT, COLOR_TEXT_DIM, COLOR_TOP_BAR,
    COLOR_OVERLAY, OVERLAY_ALPHA,
    FONT_TOPBAR_SIZE, FONT_BANNER_SIZE, FONT_GAMEOVER_SIZE,
)
from gui.ui_helpers import draw_vertical_gradient
from game.board import BLACK, WHITE

DISC_RADIUS = CELL_SIZE // 2 - 8
HINT_RADIUS = 6

_topbar_font = None
_topbar_font_small = None
_banner_font = None
_gameover_font = None


def _get_topbar_font(small=False):
    global _topbar_font, _topbar_font_small
    if small:
        if _topbar_font_small is None:
            _topbar_font_small = pygame.font.SysFont("segoeui", FONT_TOPBAR_SIZE - 4)
        return _topbar_font_small
    if _topbar_font is None:
        _topbar_font = pygame.font.SysFont("segoeui", FONT_TOPBAR_SIZE, bold=True)
    return _topbar_font


def _get_banner_font():
    global _banner_font
    if _banner_font is None:
        _banner_font = pygame.font.SysFont("segoeui", FONT_BANNER_SIZE, bold=True)
    return _banner_font


def _get_gameover_font():
    global _gameover_font
    if _gameover_font is None:
        _gameover_font = pygame.font.SysFont("georgia", FONT_GAMEOVER_SIZE, bold=True)
    return _gameover_font


def draw_board(surface):
    board_pixel_size = BOARD_SIZE * CELL_SIZE
    border_thickness = 10

    outer_rect = pygame.Rect(
        BOARD_ORIGIN_X - border_thickness, BOARD_ORIGIN_Y - border_thickness,
        board_pixel_size + border_thickness * 2, board_pixel_size + border_thickness * 2,
    )
    pygame.draw.rect(surface, COLOR_BOARD_BORDER, outer_rect, border_radius=10)

    felt_rect = pygame.Rect(BOARD_ORIGIN_X, BOARD_ORIGIN_Y, board_pixel_size, board_pixel_size)
    draw_vertical_gradient(surface, felt_rect, COLOR_BOARD_TOP, COLOR_BOARD_BOTTOM)

    for i in range(BOARD_SIZE + 1):
        x = BOARD_ORIGIN_X + i * CELL_SIZE
        pygame.draw.line(surface, COLOR_GRID_LINE, (x, BOARD_ORIGIN_Y), (x, BOARD_ORIGIN_Y + board_pixel_size))
        y = BOARD_ORIGIN_Y + i * CELL_SIZE
        pygame.draw.line(surface, COLOR_GRID_LINE, (BOARD_ORIGIN_X, y), (BOARD_ORIGIN_X + board_pixel_size, y))


def _cell_center(row, col):
    x = BOARD_ORIGIN_X + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_ORIGIN_Y + row * CELL_SIZE + CELL_SIZE // 2
    return x, y


def _draw_disc(surface, center, base_color, shine_color):
    x, y = center
    r = DISC_RADIUS

    shadow = pygame.Surface((r * 2 + 6, r * 2 + 6), pygame.SRCALPHA)
    pygame.draw.circle(shadow, (0, 0, 0, 80), (r + 3, r + 3), r)
    surface.blit(shadow, (x - r - 3 + 2, y - r - 3 + 3))

    pygame.draw.circle(surface, base_color, (x, y), r)
    rim_color = tuple(max(0, c - 30) for c in base_color)
    pygame.draw.circle(surface, rim_color, (x, y), r, 2)

    shine_radius = max(2, r // 4)
    pygame.draw.circle(surface, shine_color, (x - r // 3, y - r // 3), shine_radius)


def draw_pieces(surface, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            value = board.grid[row][col]
            if value == BLACK:
                _draw_disc(surface, _cell_center(row, col), COLOR_BLACK_DISC_BOTTOM, COLOR_BLACK_DISC_TOP)
            elif value == WHITE:
                _draw_disc(surface, _cell_center(row, col), COLOR_WHITE_DISC_BOTTOM, (255, 255, 255))


def draw_valid_moves(surface, moves):
    for row, col in moves:
        cx, cy = _cell_center(row, col)
        glow = pygame.Surface((HINT_RADIUS * 4, HINT_RADIUS * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*COLOR_ACCENT, 60), (HINT_RADIUS * 2, HINT_RADIUS * 2), HINT_RADIUS * 2)
        surface.blit(glow, (cx - HINT_RADIUS * 2, cy - HINT_RADIUS * 2))
        pygame.draw.circle(surface, COLOR_ACCENT, (cx, cy), HINT_RADIUS)


def _format_elapsed(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def draw_top_bar(surface, turn_symbol, mode_label, elapsed_seconds):
    bar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT)
    pygame.draw.rect(surface, COLOR_TOP_BAR, bar_rect)
    pygame.draw.line(surface, COLOR_ACCENT, (0, TOP_BAR_HEIGHT), (WINDOW_WIDTH, TOP_BAR_HEIGHT), 1)

    disc_color = COLOR_BLACK_DISC_BOTTOM if turn_symbol == "B" else COLOR_WHITE_DISC_BOTTOM
    pygame.draw.circle(surface, disc_color, (28, TOP_BAR_HEIGHT // 2), 10)
    pygame.draw.circle(surface, COLOR_ACCENT, (28, TOP_BAR_HEIGHT // 2), 10, 1)

    turn_text = "Black to move" if turn_symbol == "B" else "White to move"
    text = _get_topbar_font().render(turn_text, True, COLOR_TEXT)
    surface.blit(text, (48, TOP_BAR_HEIGHT // 2 - text.get_height() // 2))

    timer_text = _get_topbar_font(small=True).render(_format_elapsed(elapsed_seconds), True, COLOR_TEXT_DIM)
    surface.blit(timer_text, (48 + text.get_width() + 14, TOP_BAR_HEIGHT // 2 - timer_text.get_height() // 2))

    mode_text = _get_topbar_font(small=True).render(mode_label, True, COLOR_TEXT_DIM)
    mode_rect = mode_text.get_rect(center=(WINDOW_WIDTH // 2, TOP_BAR_HEIGHT // 2))
    surface.blit(mode_text, mode_rect)

def draw_pass_banner(surface, message):
    font = _get_banner_font()
    banner_height = 30
    banner_rect = pygame.Rect(BOARD_ORIGIN_X + 10, BOARD_ORIGIN_Y + 10, BOARD_SIZE * CELL_SIZE - 20, banner_height)

    banner_surf = pygame.Surface(banner_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(banner_surf, (0, 0, 0, 170), banner_surf.get_rect(), border_radius=6)
    surface.blit(banner_surf, banner_rect.topleft)

    text = font.render(message, True, COLOR_ACCENT)
    surface.blit(text, text.get_rect(center=banner_rect.center))


def draw_game_over(surface, black_count, white_count, winner):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*COLOR_OVERLAY, OVERLAY_ALPHA))
    surface.blit(overlay, (0, 0))

    if winner is None:
        result_text = "Draw"
    elif winner == BLACK:
        result_text = "Black wins"
    else:
        result_text = "White wins"

    title = _get_gameover_font().render(result_text, True, COLOR_ACCENT)
    surface.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 90)))

    score = _get_topbar_font().render(f"Black {black_count}  -  {white_count} White", True, COLOR_TEXT)
    surface.blit(score, score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 48)))
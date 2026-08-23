"""
menu.py

Step 12: adds "Continue Saved Game" as the first option on the mode-select
screen, but only when a save actually exists. Picking it short-circuits
mode/difficulty selection entirely -- main.py loads the real GameState
and choice from disk instead of building a fresh game.
"""

import sys
import pygame

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_MENU_BG_TOP, COLOR_MENU_BG_BOTTOM,
    COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ACCENT,
    FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BUTTON_SIZE,
)
from gui.ui_helpers import draw_vertical_gradient, Button
from game.save_load import save_exists

BUTTON_WIDTH = 280
BUTTON_HEIGHT = 54
BUTTON_GAP = 18


def _centered_buttons(items, start_y):
    x = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
    return [
        Button((x, start_y + i * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH, BUTTON_HEIGHT), label, value, FONT_BUTTON_SIZE)
        for i, (label, value) in enumerate(items)
    ]


def _run_choice_screen(screen, clock, title, subtitle, items):
    total_height = len(items) * BUTTON_HEIGHT + (len(items) - 1) * BUTTON_GAP
    start_y = WINDOW_HEIGHT // 2 - total_height // 2 + 30
    buttons = _centered_buttons(items, start_y)

    title_font = pygame.font.SysFont("georgia", FONT_TITLE_SIZE, bold=True)
    subtitle_font = pygame.font.SysFont("segoeui", FONT_SUBTITLE_SIZE)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                if button.is_clicked(event):
                    return button.value

        draw_vertical_gradient(screen, screen.get_rect(), COLOR_MENU_BG_TOP, COLOR_MENU_BG_BOTTOM)

        title_y = WINDOW_HEIGHT // 2 - total_height // 2 - 90
        title_surf = title_font.render(title, True, COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, title_y))
        pygame.draw.circle(screen, (10, 10, 10), (title_rect.left - 26, title_y), 12)
        pygame.draw.circle(screen, (240, 240, 240), (title_rect.right + 26, title_y), 12)
        screen.blit(title_surf, title_rect)

        underline_y = title_rect.bottom + 8
        pygame.draw.line(screen, COLOR_ACCENT, (WINDOW_WIDTH // 2 - 90, underline_y), (WINDOW_WIDTH // 2 + 90, underline_y), 2)

        subtitle_surf = subtitle_font.render(subtitle, True, COLOR_TEXT_DIM)
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(WINDOW_WIDTH // 2, underline_y + 26)))

        for button in buttons:
            button.draw(screen, mouse_pos, COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER, COLOR_TEXT)

        pygame.display.flip()
        clock.tick(30)


def run_menu(screen, clock):
    mode_items = []
    if save_exists():
        mode_items.append(("Continue Saved Game", "continue"))
    mode_items += [("Human vs Human", "human_vs_human"), ("Human vs AI", "human_vs_ai")]

    mode = _run_choice_screen(screen, clock, "OTHELLO", "Choose a game mode", mode_items)

    if mode == "continue":
        return {"mode": "continue"}
    if mode == "human_vs_human":
        return {"mode": mode}

    difficulty = _run_choice_screen(
        screen, clock, "OTHELLO", "Choose a difficulty",
        [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")],
    )
    return {"mode": mode, "difficulty": difficulty}
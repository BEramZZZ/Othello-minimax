import sys
import pygame

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TOP_BAR_HEIGHT, COLOR_BACKGROUND,
    COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER, COLOR_TEXT,
)
from gui.renderer import draw_board, draw_pieces, draw_valid_moves, draw_top_bar, draw_pass_banner, draw_game_over
from gui.event_handler import pixel_to_cell
from gui.menu import run_menu
from gui.ui_helpers import Button
from game.game_state import GameState
from game.board import BLACK, WHITE, SYMBOLS
from game.player import HumanPlayer, AIPlayer
from game.save_load import save_game, load_game, delete_save
from ai.difficulty import settings_for

PASS_BANNER_DURATION_MS = 1500


def build_players(choice):
    if choice["mode"] == "human_vs_human":
        return {BLACK: HumanPlayer(BLACK), WHITE: HumanPlayer(WHITE)}
    settings = settings_for(choice["difficulty"])
    ai = AIPlayer(WHITE, depth=settings["depth"], eval_fn=settings["eval_fn"])
    return {BLACK: HumanPlayer(BLACK), WHITE: ai}


def _mode_label(choice):
    if choice["mode"] == "human_vs_human":
        return "Human vs Human"
    return f"Human vs AI \u2014 {choice['difficulty'].capitalize()}"


def handle_auto_passes(state, banner_state):
    while not state.is_game_over() and not state.legal_moves():
        message = f"{SYMBOLS[state.current_player]} has no legal moves -- turn passed"
        banner_state["last_pass"] = (message, pygame.time.get_ticks())
        state.pass_turn()


def maybe_play_ai_move(state, players, banner_state):
    while not state.is_game_over() and isinstance(players[state.current_player], AIPlayer):
        move = players[state.current_player].get_move(state.board)
        state.play_move(move[0], move[1])
        handle_auto_passes(state, banner_state)


def handle_undo(state, players):
    """One Undo click = back to the human's turn, skipping over any
    AI ply(s) that happened since, not just one raw ply."""
    if not state.can_undo():
        return
    state.undo()
    while isinstance(players.get(state.current_player), AIPlayer) and state.can_undo():
        state.undo()


def _run_single_game(screen, clock, choice, preloaded_state=None):
    """One playthrough. Returns 'menu', 'restart', or 'quit'."""
    players = build_players(choice)
    mode_label = _mode_label(choice)

    state = preloaded_state if preloaded_state is not None else GameState()
    banner_state = {"last_pass": None}
    handle_auto_passes(state, banner_state)
    maybe_play_ai_move(state, players, banner_state)
    turn_started_at = pygame.time.get_ticks()

    menu_button = Button((WINDOW_WIDTH - 92, 9, 82, TOP_BAR_HEIGHT - 18), "Menu")
    save_button = Button((WINDOW_WIDTH - 92 - 8 - 70, 9, 70, TOP_BAR_HEIGHT - 18), "Save")
    undo_button = Button((WINDOW_WIDTH - 92 - 8 - 70 - 8 - 70, 9, 70, TOP_BAR_HEIGHT - 18), "Undo")
    play_again_button = Button((WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT // 2 + 10, 150, 46), "Play Again")
    main_menu_button = Button((WINDOW_WIDTH // 2 + 10, WINDOW_HEIGHT // 2 + 10, 150, 46), "Main Menu")

    save_flash_until = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if not state.is_game_over():
                if menu_button.is_clicked(event):
                    return "menu"

                if save_button.is_clicked(event):
                    save_game(state, choice)
                    save_flash_until = pygame.time.get_ticks() + 1200

                if state.can_undo() and undo_button.is_clicked(event):
                    handle_undo(state, players)
                    banner_state["last_pass"] = None
                    turn_started_at = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONDOWN and isinstance(players[state.current_player], HumanPlayer):
                    cell = pixel_to_cell(event.pos)
                    if cell is not None and cell in state.legal_moves():
                        state.play_move(cell[0], cell[1])
                        handle_auto_passes(state, banner_state)
                        maybe_play_ai_move(state, players, banner_state)
                        turn_started_at = pygame.time.get_ticks()
            else:
                if play_again_button.is_clicked(event):
                    return "restart"
                if main_menu_button.is_clicked(event):
                    return "menu"

        if state.is_game_over():
            delete_save()  # a finished game shouldn't offer "Continue"

        screen.fill(COLOR_BACKGROUND)
        draw_board(screen)
        draw_pieces(screen, state.board)

        elapsed_seconds = (pygame.time.get_ticks() - turn_started_at) // 1000
        draw_top_bar(screen, SYMBOLS[state.current_player], mode_label, elapsed_seconds)

        if not state.is_game_over():
            draw_valid_moves(screen, state.legal_moves())
            menu_button.draw(screen, mouse_pos, COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER, COLOR_TEXT)
            save_label = "Saved!" if pygame.time.get_ticks() < save_flash_until else "Save"
            Button(save_button.rect, save_label).draw(screen, mouse_pos, COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER, COLOR_TEXT)
            if state.can_undo():
                undo_button.draw(screen, mouse_pos, COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER, COLOR_TEXT)

        if banner_state["last_pass"] is not None:
            message, shown_at = banner_state["last_pass"]
            if pygame.time.get_ticks() - shown_at < PASS_BANNER_DURATION_MS:
                draw_pass_banner(screen, message)
            else:
                banner_state["last_pass"] = None

        if state.is_game_over():
            black, white = state.board.count()
            draw_game_over(screen, black, white, state.winner())
            play_again_button.draw(screen, mouse_pos, COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER, COLOR_TEXT)
            main_menu_button.draw(screen, mouse_pos, COLOR_BUTTON_BASE, COLOR_BUTTON_HOVER, COLOR_BUTTON_BORDER, COLOR_TEXT)

        pygame.display.flip()
        clock.tick(FPS)


def play_session(screen, clock, choice, preloaded_state=None):
    first = True
    while True:
        state_arg = preloaded_state if first else None
        outcome = _run_single_game(screen, clock, choice, preloaded_state=state_arg)
        first = False
        if outcome != "restart":
            return outcome


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Othello")
    clock = pygame.time.Clock()

    while True:
        choice = run_menu(screen, clock)

        if choice["mode"] == "continue":
            loaded = load_game()
            if loaded is None:
                continue  # save missing or corrupt -- back to menu, no crash
            state, saved_choice = loaded
            outcome = play_session(screen, clock, saved_choice, preloaded_state=state)
        else:
            outcome = play_session(screen, clock, choice)

        if outcome == "quit":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
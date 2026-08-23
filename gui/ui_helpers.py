import pygame


def draw_vertical_gradient(surface, rect, top_color, bottom_color):
    """Fill `rect` with a top-to-bottom gradient, one line per pixel row."""
    x, y, w, h = rect
    if h <= 0:
        return
    for i in range(h):
        t = i / h
        color = tuple(int(top_color[c] + (bottom_color[c] - top_color[c]) * t) for c in range(3))
        pygame.draw.line(surface, color, (x, y + i), (x + w, y + i))


class Button:
    """A rounded, hover-highlighted, click-detecting button."""

    def __init__(self, rect, label, value=None, font_size=26):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.font_size = font_size
        self._font = None

    def _get_font(self):
        if self._font is None:
            self._font = pygame.font.SysFont("segoeui", self.font_size, bold=True)
        return self._font

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface, mouse_pos, base_color, hover_color, border_color, text_color):
        hovered = self.is_hovered(mouse_pos)
        color = hover_color if hovered else base_color

        shadow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 60), shadow.get_rect(), border_radius=10)
        surface.blit(shadow, self.rect.move(0, 3).topleft)

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        if hovered:
            pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=10)

        text = self._get_font().render(self.label, True, text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
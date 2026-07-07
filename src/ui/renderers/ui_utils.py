import pygame
from typing import Optional


def draw_window(
    surface: pygame.Surface,
    title: str,
    sub_title: Optional[str],
    font_name: str,
    font_size: int,
    padding: int,
    width: Optional[int] = None,
    height: Optional[int] = None,
    x: Optional[int] = None,
    y: Optional[int] = None,
):
    if not width:
        w = surface.get_width()
        window_width = w / 2
    else:
        window_width = width

    if not height:
        h = surface.get_height()
        window_height = h / 2
    else:
        window_height = height

    if x is None:
        x = (surface.get_width() / 2) - (window_width / 2)
    if y is None:
        y = (surface.get_height() / 2) - (window_height / 2)

    panel_rect = pygame.Rect(x, y, window_width, window_height)
    pygame.draw.rect(surface, (30, 30, 30), panel_rect)
    pygame.draw.rect(surface, (255, 255, 255), panel_rect, 2)

    title_font = ensure_font_fits(
        title, font_name, font_size, window_width - 2 * padding
    )
    title_render = title_font.render(title, True, "white")
    surface.blit(title_render, (panel_rect.x + padding, panel_rect.y + padding))

    if sub_title:
        sub_font_size = int(font_size/ 2)
        sub_title_font = ensure_font_fits(
            sub_title, font_name, sub_font_size, window_width - 2 * padding
        )
        sub_title_render = sub_title_font.render(
            sub_title, True, "white"
        )
        surface.blit(
            sub_title_render,
            (panel_rect.x + padding, panel_rect.y + padding + font_size + 5),
        )

    return panel_rect

def ensure_font_fits(text: str, font_name: str, font_size: int, max_width: int) -> pygame.font.Font:
    """
    Adjusts the font size to ensure the text fits within the specified max_width.
    Returns a new font object with the adjusted size.
    """
    font = pygame.font.SysFont(font_name, font_size)
    while font.size(text)[0] > max_width and font_size > 1:
        font_size -= 1
        font = pygame.font.SysFont(font_name, font_size)
    return font


def draw_underscores(surface: pygame.Surface, start_x: int, start_y: int, length: int, font_width):
    score_width = max(1, int(font_width * 0.85))
    score_gap = max(1, int(font_width * 0.24))

    for i in range(length):
        x = start_x + i * (score_width + score_gap)

        pygame.draw.line(
            surface,
            "white",
            (x, start_y),
            (x + score_width, start_y),
            2,
        )

def draw_cursor(surface: pygame.Surface, pos_x: int, pos_y: int, cursor_width: int = 2, cursor_height: int = 20):
    pygame.draw.line(
        surface,
        "white",
        (pos_x, pos_y),
        (pos_x, pos_y + cursor_height),
        cursor_width,
    )
import pygame
from typing import Optional


def draw_window(
    surface: pygame.Surface,
    title: str,
    sub_title: Optional[str],
    font: pygame.font.Font,
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

    title = font.render(title, True, "white")

    surface.blit(title, (panel_rect.x + padding, panel_rect.y + padding))
    if sub_title:
        font_size = font.point_size
        sub_font_size = int(font_size / 2)
        sub_title_render = pygame.font.SysFont(font.name, sub_font_size).render(
            sub_title, True, "white"
        )
        surface.blit(
            sub_title_render,
            (panel_rect.x + padding, panel_rect.y + padding + font_size),
        )

    return panel_rect

import pygame
from typing import Optional


def draw_window(
    surface: pygame.Surface,
    title: str,
    sub_title: Optional[str],
    font: pygame.font.Font,
    padding: int,
):
    # TODO: Abstract this size section
    w = surface.get_width()
    h = surface.get_height()
    window_width = w / 2
    window_height = h / 2
    x = (w / 2) - (window_width / 2)
    y = (h / 2) - (window_height / 2)

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

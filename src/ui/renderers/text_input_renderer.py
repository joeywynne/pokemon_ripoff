import pygame
from src.ui.renderers import ui_utils as utils


class TextInputRenderer:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 24)
        self.row_height = 32
        self.padding = 10
        self.title_gap = 150
        self.first_visible_row = 0
        self.height = 200

    def render(self, surface: pygame.Surface, text: str):
        sub_title = "Enter the new name and press Enter. Press Esc to cancel."
        window_panel = utils.draw_window(
            surface=surface,
            title="Rename Pokémon",
            sub_title=sub_title,
            font=self.font,
            padding=self.padding,
            height=self.height
        )
        text = self.font.render(text, True, "white")
        surface.blit(text, (window_panel.x + 15, window_panel.y + self.title_gap))

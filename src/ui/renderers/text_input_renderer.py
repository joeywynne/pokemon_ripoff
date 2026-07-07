import pygame
from src.ui.renderers import ui_utils as utils
from src.ui.ui_handler import UIScreen

class TextInputRenderer:
    def __init__(self):
        self.font_name = "consolas"
        self.font_size = 26
        self.padding = 20
        self.height = 200

    def render(self, surface: pygame.Surface, modal: UIScreen):
        sub_title = "Enter the new name and press Enter.\nPress Esc to cancel."
        font = pygame.font.SysFont(self.font_name, self.font_size)
        window_panel = utils.draw_window(
            surface=surface,
            title="Rename Pokémon",
            sub_title=sub_title,
            font_name=self.font_name,
            font_size=self.font_size,
            padding=self.padding,
            height=self.height
        )
        y_offset = window_panel.height / 2
        text = font.render(modal.text, True, "white")
        text_x = window_panel.x + self.padding
        text_y = window_panel.y + y_offset
        surface.blit(text, (text_x, text_y))
        
        utils.draw_underscores(
            surface,
            text_x,
            text_y + 30,
            modal.max_length,
            font.size(" ")[0]
        )

        if modal.cursor_visible:
            text_width = font.size(modal.text)[0]
            cursor_x = text_x + text_width + 3
            utils.draw_cursor(
                surface,
                cursor_x,
                text_y,
                cursor_width=3,
                cursor_height=self.font_size
            )
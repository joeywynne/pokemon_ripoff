import pygame
from src.ui.renderers import ui_utils as utils


class PartyRenderer:
    def __init__(self):
        self.font_name = "consolas"
        self.font_size = 24
        self.row_height = 32
        self.padding = 10
        self.title_gap = 50
        self.first_visible_row = 0

    def render(self, surface: pygame.Surface, party_screen):
        sub_title = "Up/down to navigate.\nSpace to select/deselect your Buddy."
        window_panel = utils.draw_window(
            surface=surface,
            title="Current Party",
            sub_title=sub_title,
            font_name=self.font_name,
            font_size=self.font_size,
            padding=self.padding,
        )
        self.draw_rows(surface, window_panel, party_screen.game_state, party_screen)

    def draw_rows(self, surface: pygame.Surface, panel, game_state, party_screen):
        start_y = panel.y + self.title_gap * 1.30
        num_rows = self.get_visible_rows(panel.height, party_screen.selected_index)

        for row_index, pokemon_index in enumerate(
            range(self.first_visible_row, self.first_visible_row + num_rows)
        ):
            if pokemon_index > len(game_state.party) - 1:
                break
            pokemon = game_state.party[pokemon_index]
            row_y = start_y + row_index * self.row_height

            # Highlight selected row
            if pokemon_index == party_screen.selected_index:
                highlight = pygame.Rect(
                    panel.x + 5, row_y, panel.width - 10, self.row_height
                )
                pygame.draw.rect(surface, (70, 70, 140), highlight)

            row_text = pokemon.name
            font = pygame.font.SysFont(self.font_name, self.font_size)
            text = font.render(row_text, True, "white")
            surface.blit(text, (panel.x + 15, row_y + 4))

            if pokemon_index == party_screen.buddy_index:
                available_width = panel.width - 2 * self.padding
                marker = pygame.font.SysFont(self.font_name, self.font_size).render("(*)", True, "white")
                surface.blit(marker, (panel.x + 15 + available_width - marker.get_width(), row_y + 4))
                

    def get_visible_rows(self, panel_size, selected_index) -> int:
        usable_height = panel_size - self.title_gap - self.padding
        num_rows = usable_height // self.row_height

        start = self.first_visible_row
        end = start + num_rows
        if selected_index >= end:
            self.first_visible_row = selected_index - num_rows + 1
        elif selected_index < start:
            self.first_visible_row = selected_index
        return num_rows

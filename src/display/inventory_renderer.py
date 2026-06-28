import pygame
from src.menu.inventory_screen import InventoryScreen


class InventoryRenderer:

    def __init__(self, screen: pygame.Surface):
        self.font = pygame.font.SysFont("consolas", 24)
        self.row_height = 32
        self.padding = 10
        self.title_gap = 50
        self.screen = screen
        self.first_visible_row = 0

    def render(self, game_state, inventory_screen: InventoryScreen):
        window_panel = self.draw_window(title="Current Party")
        self.draw_rows(window_panel, game_state, inventory_screen)

    def draw_rows(self, panel, game_state, inventory_screen):
        start_y = panel.y + self.title_gap
        num_rows = self.get_visible_rows(panel.height, inventory_screen.selected_index)

        for row_index, pokemon_index in enumerate(
            range(self.first_visible_row, self.first_visible_row + num_rows)
            ):
            if pokemon_index > len(game_state.party) - 1:
                break
            pokemon = game_state.party[pokemon_index]
            row_y = start_y + row_index * self.row_height

            # Highlight selected row
            if pokemon_index == inventory_screen.selected_index:
                highlight = pygame.Rect(
                    panel.x + 5,
                    row_y,
                    panel.width - 10,
                    self.row_height
                )
                pygame.draw.rect(self.screen, (70, 70, 140), highlight)

            row_text = pokemon.name
            print(pokemon_index, inventory_screen.buddy_index)
            if pokemon_index == inventory_screen.buddy_index:
                row_text = f"{row_text}     (*)"
            text = self.font.render(row_text, True, "white")
            self.screen.blit(text, (panel.x + 15, row_y + 4))

        
    def draw_window(self, title: str):
        w = self.screen.width
        h = self.screen.height
        window_width = w / 2
        window_height = h / 2
        x = (w / 2) - (window_width / 2)
        y = (h / 2) - (window_height / 2)

        panel_rect = pygame.Rect(x, y, window_width, window_height)
        pygame.draw.rect(self.screen, (30, 30, 30), panel_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect, 2)

        title = self.font.render(title, True, "white")
        self.screen.blit(title, (panel_rect.x + self.padding, panel_rect.y + self.padding))

        return panel_rect

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

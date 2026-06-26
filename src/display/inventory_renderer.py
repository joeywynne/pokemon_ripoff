import pygame


class InventoryRenderer:

    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 24)

    def render(self, surface, game_state):
        panel_rect = pygame.Rect(100, 50, 400, 500)
        pygame.draw.rect(surface, (30, 30, 30), panel_rect)
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, 2)

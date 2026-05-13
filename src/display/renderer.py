import pygame
from src.core.settings import BLACK, RED, WHITE
from src.entities.player import Player

class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def clear(self):
        "Fill screen with background colour"
        self.screen.fill(BLACK)

    def render(self, player: Player):
        pygame.draw.rect(self.screen, RED, player.get_rect())
        pygame.display.flip()
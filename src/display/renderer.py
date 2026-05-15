import pygame
from src.core.settings import BLACK, RED
from src.display.map_renderer import MapRenderer
from src.display.entities_renderer import EntitiesRenderer
from src.entities.player import Entity

class Renderer:
    def __init__(
        self,
        screen: pygame.Surface,
        entities_renderer: EntitiesRenderer,
        map_renderer: MapRenderer
    ):
        self.screen = screen
        self.entities_renderer = entities_renderer
        self.map_renderer = map_renderer

    def render(self):
        self.screen.fill(BLACK)
        self.entities_renderer.draw(self.screen)
        self.map_renderer.draw(self.screen)
        pygame.display.flip()

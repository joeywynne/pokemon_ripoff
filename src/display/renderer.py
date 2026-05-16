import pygame
from src.core.settings import BLACK
from src.display.map_renderer import MapRenderer
from src.display.entities_renderer import EntitiesRenderer
from src.entities.player import Player
from src.core.camera import Camera

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

    def render(self, player: Player, camera: Camera):
        self.screen.fill(BLACK)
        camera.follow(player.get_rect())
        self.entities_renderer.draw(self.screen, camera)
        self.map_renderer.draw(self.screen, camera)
        pygame.display.flip()

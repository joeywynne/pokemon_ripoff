import pygame
from typing import Optional
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

    def render(self, player: Player, camera: Camera, fps_text: Optional[pygame.Surface] = None, debug: Optional[bool] = False):
        self.screen.fill(BLACK)
        camera.follow(player.get_rect())
        # Draw map first, then entities on top so the player is visible.
        self.map_renderer.draw(self.screen, camera)
        self.entities_renderer.draw(self.screen, camera, debug)

        if fps_text is not None:
            text_width = fps_text.get_width()
            text_height = fps_text.get_height()
            padding = 8
            box_rect = pygame.Rect(8, 8, text_width + padding * 2, text_height + padding)
            pygame.draw.rect(self.screen, (0, 0, 0), box_rect)
            self.screen.blit(fps_text, (8 + padding, 8 + padding))

        pygame.display.flip()

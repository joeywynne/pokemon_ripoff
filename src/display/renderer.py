import pygame
from typing import Optional
from src.core import camera
from src.core.settings import BLACK, GREEN, MAX_THROW_POWER, RED
from src.display.map_renderer import MapRenderer
from src.display.entities_renderer import EntitiesRenderer
from src.entities.player import Player
from src.core.camera import Camera
from src.display.assets import AssetStore
from src.entities.pokemon import Pokemon


class Renderer:
    def __init__(
        self,
        screen: pygame.Surface,
        entities_renderer: EntitiesRenderer,
        map_renderer: MapRenderer,
    ):
        self.screen = screen
        self.entities_renderer = entities_renderer
        self.map_renderer = map_renderer

    def render(
        self,
        player: Player,
        camera: Camera,
        fps_text: Optional[pygame.Surface] = None,
        debug: Optional[bool] = False,
    ):
        self.screen.fill(BLACK)
        camera.follow(player.get_rect(), player.velocity)
        # Draw map first, then entities on top so the player is visible.
        self.map_renderer.draw(self.screen, camera)
        self.entities_renderer.draw(self.screen, camera, player.target, debug)

        if player.throw_preview_points:
            self.draw_trajectory(
                player.throw_preview_points, camera, player.render_throw_power
            )

        if fps_text is not None:
            text_width = fps_text.get_width()
            text_height = fps_text.get_height()
            padding = 8
            box_rect = pygame.Rect(
                8, 8, text_width + padding * 2, text_height + padding
            )
            pygame.draw.rect(self.screen, (0, 0, 0), box_rect)
            self.screen.blit(fps_text, (8 + padding, 8 + padding))

        pygame.display.flip()

    def draw_trajectory(self, points, camera, power):
        for x, y in points[::3]:
            screen_x = x - camera.x
            screen_y = y - camera.y

            if power < MAX_THROW_POWER * 0.25:
                power_colour = GREEN
            elif power < MAX_THROW_POWER * 0.50:
                power_colour = (255, 165, 0)
            else:
                power_colour = RED

            pygame.draw.circle(
                self.screen, power_colour, (int(screen_x), int(screen_y)), 3
            )

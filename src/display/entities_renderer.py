from typing import Optional
import pygame
from src.display.assets import AssetStore
from src.entities.entity import Entity
from src.entities.pokeball import Projectile
from src.core.camera import Camera


class EntitiesRenderer:
    def __init__(self, entities: list[Entity], assets: AssetStore):
        self.entities = entities
        self.assets = assets

    def draw_entity(
        self,
        surface: pygame.Surface,
        entity: Entity,
        camera: Camera,
        debug: Optional[bool] = False,
    ):
        scale_y = 1
        scale_x = 1
        if isinstance(entity, Projectile):
            behaviour = entity.movement_controller
            if behaviour.vz < 0:
                scale_y = 0.95
                scale_x = 1.05
            elif entity.squash_timer > 0:
                scale_y = 0.75
                scale_x = 1.15
            shadow_pos = (
                int(entity.x - camera.x + entity.size * 0.5),
                int(entity.y - camera.y + entity.size),
            )
            pygame.draw.circle(
                surface, (50, 50, 50), shadow_pos, entity.size // 3
            )  # Draw shadow as a circle

        rect = entity.get_rect()
        screen_rect = rect.move(-int(camera.x), -int(camera.y))
        if getattr(entity, "sprite_info", None):
            sprite = self.assets.get_sprite(
                entity.sprite_info.relative_path,
                entity.size,
                position=entity.sprite_info.position,
                sprite_size=entity.sprite_info.sprite_size,
            )
            
            sprite = pygame.transform.rotate(sprite, entity.rotation)
            sprite = pygame.transform.scale(
                sprite, (int(entity.size * scale_x), int(entity.size * scale_y))
            )

            sprite_rect = sprite.get_rect()
            sprite_rect.center = (
                screen_rect.centerx,
                screen_rect.centery - int(entity.z * 1.0),
            )

            surface.blit(sprite, sprite_rect)
        else:
            pygame.draw.rect(surface, entity.colour, screen_rect)

        if debug:
            pygame.draw.rect(
                surface, (255, 0, 0), screen_rect, 1
            )  # Red outline for debugging

    def draw(
        self, surface: pygame.Surface, camera: Camera, debug: Optional[bool] = False
    ):
        for entity in self.entities:
            self.draw_entity(surface, entity, camera, debug)

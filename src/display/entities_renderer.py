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
        if isinstance(entity, Projectile):
            if entity.z < 0.5:
                scale_y = 0.8
            shadow_pos = (
                int(entity.x - camera.x + entity.size * 0.5),
                int(entity.y - camera.y + entity.size),
            )
            pygame.draw.circle(surface, (50, 50, 50), shadow_pos, entity.size // 2)  # Draw shadow as a circle

        rect = entity.get_rect()
        screen_rect = rect.move(-int(camera.x), -int(camera.y))
        if getattr(entity, "sprite_info", None):
            sprite = self.assets.get_sprite(
                entity.sprite_info.relative_path,
                entity.size,
                position=entity.sprite_info.position,
                sheet_size=entity.sprite_info.sheet_size,
            )
            sprite = pygame.transform.scale(sprite, (entity.size, int(entity.size * scale_y)))
            sprite_rect = sprite.get_rect()
            sprite_rect.center = (screen_rect.centerx, screen_rect.centery - int(entity.z * 1.0))
    
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

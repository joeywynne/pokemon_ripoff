from typing import Optional
import pygame
from src.display.assets import AssetStore
from src.entities.entity import Entity
from src.core.camera import Camera

class EntitiesRenderer:
    def __init__(self, entities: list[Entity], assets: AssetStore):
        self.entities = entities
        self.assets = assets

    def draw_entity(self, surface: pygame.Surface, entity: Entity, camera: Camera, debug: Optional[bool] = False):
        rect = entity.get_rect()
        screen_rect = rect.move(-int(camera.x), -int(camera.y))
        if getattr(entity, "sprite_info", None):
            sprite = self.assets.get_sprite(
                entity.sprite_info.relative_path,
                position=entity.sprite_info.position,
                size=entity.sprite_info.size
            )
            sprite_rect = sprite.get_rect()
            sprite_rect.center = screen_rect.center
            surface.blit(sprite, sprite_rect)
        else:
            pygame.draw.rect(surface, entity.colour, screen_rect)

        if debug:
            pygame.draw.rect(surface, (255, 0, 0), screen_rect, 1)  # Red outline for debugging
        
    
    def draw(self, surface: pygame.Surface, camera: Camera, debug: Optional[bool] = False):
        for entity in self.entities:
            self.draw_entity(surface, entity, camera, debug)

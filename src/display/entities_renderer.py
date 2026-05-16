import pygame
from src.display.assets import AssetStore
from src.entities.player import Entity
from src.core.camera import Camera

class EntitiesRenderer:
    def __init__(self, entities: list[Entity], assets: AssetStore):
        self.entities = entities
        self.assets = assets

    def draw_entity(self, surface: pygame.Surface, entity: Entity, camera: Camera):
        rect = entity.get_rect()
        screen_rect = rect.move(-int(camera.x), -int(camera.y))
        if getattr(entity, "sprite", None):
            sprite = self.assets.image(entity.sprite, alpha=True)
            surface.blit(sprite, screen_rect)
        else:
            pygame.draw.rect(surface, entity.colour, screen_rect)
        
    
    def draw(self, surface: pygame.Surface, camera: Camera):
        for entity in self.entities:
            self.draw_entity(surface, entity, camera)

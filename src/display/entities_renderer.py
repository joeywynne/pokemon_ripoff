import pygame
from src.entities.player import Entity

class EntitiesRenderer:
    def __init__(self, entities: list[Entity]):
        self.entities = entities
    
    def draw(self, surface: pygame.Surface):
        for entity in self.entities:
            pygame.draw.rect(surface, entity.colour, entity.get_rect())

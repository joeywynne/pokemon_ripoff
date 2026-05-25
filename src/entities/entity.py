import pygame
from src.core.map.collision_map import CollisionMap
from typing import Optional

class Entity:
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.colour = colour
        self.sprite: Optional[str] = None
    
    @property
    def facing(self) -> tuple[int, int]:
        # Determine facing direction based on velocity
        if self.velocity[0] > 0:
            return (1, 0)  # Facing right
        elif self.velocity[0] < 0:
            return (-1, 0) # Facing left
        else:
            return (1, 0)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def get_move(self, **kwargs) -> tuple[float, float]:
        # Default to no movement
        return 0, 0
    
    def update(self, collision_map: CollisionMap, **kwargs):
        dx, dy = self.get_move(**kwargs)
        
        if dx != 0 and dy != 0:
            dx *= 0.7071   # ≈ 1/sqrt(2)
            dy *= 0.7071
        
        target_x = self.x + dx
        target_rect = pygame.Rect(target_x, self.y, self.size, self.size)
        if can_move_to(target_rect, collision_map):
            self.x = target_x
            self.velocity[0] = dx
        
        target_y = self.y + dy
        target_rect = pygame.Rect(self.x, target_y, self.size, self.size)
        if can_move_to(target_rect, collision_map):
            self.y = target_y
            self.velocity[1] = dy  


def can_move_to(target_rect: pygame.Rect, collision_map: CollisionMap) -> bool:
    return not collision_map.collides(target_rect)

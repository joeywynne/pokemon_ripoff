import pygame
from src.core.map.collision_map import CollisionMap
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED
from typing import Optional

class Entity:
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.colour = colour
        self.sprite: Optional[str] = None
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Player(Entity):
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.colour = colour
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.sprite: Optional[str] = "entities/ditto.png"

    def update(self, keys, collision_map: CollisionMap):
        "Update the player's position based on the pressed keys."
        dy, dx = 0, 0  # Default to no movement if no movement keys are pressed
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]: 
            dy += self.speed

        target_pos = (self.x + dx, self.y + dy)
        negative_pos = (self.x - dx, self.y - dy)
        target_rect = pygame.Rect(self.x + dx, self.y + dy, self.size, self.size)
        final_pos = target_pos if can_move_to(target_rect, collision_map) else negative_pos
        self.x, self.y = final_pos

def can_move_to(target_rect: pygame.Rect, collision_map: CollisionMap) -> bool:
    return not collision_map.collides(target_rect)

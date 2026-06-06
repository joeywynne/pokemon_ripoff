from src.entities.entity import Entity
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED
from typing import Optional
import pygame

class Player(Entity):
    def __init__(self, x: int, y: int, colour: tuple):
        super().__init__(x, y, colour)
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.sprite: Optional[str] = "entities/ditto.png"

    def get_intended_move(self, keys: dict) -> tuple[float, float]:
        dy, dx = 0, 0  # Default to no movement if no movement keys are pressed
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]: 
            dy += self.speed

        return dx, dy

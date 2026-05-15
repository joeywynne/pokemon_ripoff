import pygame
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED

class Entity:
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.colour
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Player(Entity):
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.colour = colour
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED

    def update(self, keys):
        "Update the player's position based on the pressed keys."
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.y += PLAYER_SPEED

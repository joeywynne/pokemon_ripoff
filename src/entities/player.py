import pygame
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
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

    def get_rect(self):
        "Return the player's rectangle for rendering."
        return pygame.Rect(self.x, self.y, self.size, self.size)
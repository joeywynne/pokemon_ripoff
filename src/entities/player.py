from src.entities.entity import Entity, SpriteInfo
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED, RED
import pygame
from pathlib import Path

from src.entities.pokeball import Pokeball


class Player(Entity):
    def __init__(self, x: int, y: int, colour: tuple):
        super().__init__(x, y, colour)
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        ditto_info = SpriteInfo(relative_path=Path("entities/ditto.png"))
        self.sprite_info = ditto_info

        self.throw_charge = 0
        self.throwing = False
        self.cool_down = 0  # todo

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

        pokeball = None
        if keys[pygame.K_SPACE]:
            # Pokeball time!
            self.charge_pokeball()
        else:
            # Need to check if we can now throw a ball
            pokeball = self.throw_pokeball()

        return dx, dy, pokeball

    def charge_pokeball(self):
        if not self.throwing:
            self.throwing = True
        self.throw_charge += 1

    def throw_pokeball(self):
        if not self.throwing:
            return  # Not currently charging, so nothing to throw

        power = self.throw_charge
        # Create a pokeball entity with speed based on charge
        # and direction based on facing
        pokeball = Pokeball(self.x, self.y, RED, facing=self.facing, throw_power=power)

        self.throwing = False
        self.throw_charge = 0
        return pokeball

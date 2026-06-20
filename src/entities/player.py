from src.entities.entity import Entity, SpriteInfo
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED, RED
import pygame
from pathlib import Path

from src.entities.pokeball import Pokeball
from src.movement.behaviour import PlayerBehaviour


class Player(Entity):

    def __init__(self, x: int, y: int, colour: tuple):
        super().__init__(
            x,
            y,
            PLAYER_SIZE,
            1.0,
            PLAYER_SPEED,
            get_player_sprite_info(),
            movement_controller=PlayerBehaviour()
        )

        self.throw_charge = 0
        self.throwing = False
        self.cool_down = 0  # todo

    def update_intended(self, keys: dict) -> Pokeball | None:
        pokeball = None
        if keys[pygame.K_SPACE]:
            # Pokeball time!
            self.charge_pokeball()
        else:
            # Need to check if we can now throw a ball
            pokeball = self.throw_pokeball()

        if self.cool_down > 0:
            self.cool_down -= 1

        super().update_intended(keys=keys)
        return pokeball

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
        pokeball = Pokeball(self.x, self.y, facing=self.facing, throw_power=power)

        self.throwing = False
        self.throw_charge = 0
        return pokeball


def get_player_sprite_info() -> SpriteInfo:
    return SpriteInfo(relative_path=Path("entities/ditto.png"))

from typing import Optional

from src.entities.entity import Entity, SpriteInfo
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED, RED
import pygame
from pathlib import Path

from src.entities.pokeball import Pokeball
from src.entities.pokemon import Pokemon
from src.movement.behaviour import PlayerBehaviour
from src.targetting_system import get_pokeball_trajectory, find_target


class Player(Entity):

    def __init__(self, x: int, y: int, colour: tuple):
        super().__init__(
            x,
            y,
            PLAYER_SIZE,
            1.0,
            PLAYER_SPEED,
            get_player_sprite_info(),
            movement_controller=PlayerBehaviour(),
        )

        self.throw_charge = 0
        self.throwing = False
        self.target: Optional[Pokemon] | None = None
        self.throw_preview_points = []
        self.render_throw_power = 0.0
        self.vision_distance = 200
        self.vision_angle = 60

    def update_intended(
        self, keys: dict, pokemon: list[Pokemon], **kwargs
    ) -> Pokeball | None:
        self.target = find_target(
            self.x,
            self.y,
            self.facing,
            self.vision_angle,
            self.vision_distance,
            pokemon,
        )
        pokeball = None
        if keys[pygame.K_SPACE]:
            # Pokeball time!
            self.charge_pokeball()
            self.throw_preview_points = get_pokeball_trajectory(
                self.x, self.y, self.facing, self.throw_charge
            )
            self.render_throw_power = self.throw_charge
        else:
            # Need to check if we can now throw a ball
            pokeball = self.throw_pokeball()

        super().update_intended(keys=keys)
        return pokeball

    def charge_pokeball(self):
        if not self.throwing:
            self.throwing = True
        self.throw_charge += 1

    def throw_pokeball(self):
        if not self.throwing:
            return

        power = self.throw_charge
        # Create a pokeball entity with speed based on charge
        # and direction based on facing
        pokeball = Pokeball(self.x, self.y, facing=self.facing, throw_power=power)

        self.throwing = False
        self.throw_charge = 0
        return pokeball


def get_player_sprite_info() -> SpriteInfo:
    return SpriteInfo(relative_path=Path("entities/ditto.png"))

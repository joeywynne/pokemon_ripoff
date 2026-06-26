from typing import Optional

from src.entities.entity import Entity, SpriteInfo
from src.core.settings import PLAYER_SIZE, PLAYER_SPEED
import pygame
from pathlib import Path

from src.entities.pokeball import Pokeball
from src.entities.pokemon import Pokemon
from src.movement.behaviour import PlayerBehaviour
from src.targetting_system import get_pokeball_trajectory, find_target
from src.movement.movement_system import normalise_vector


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

    def update_intended(self, update_context) -> Pokeball | None:
        self.target = find_target(
            self.x,
            self.y,
            self.facing,
            self.vision_angle,
            self.vision_distance,
            update_context.pokemon,
        )
        pokeball = None
        keys = update_context.keys
        if keys[pygame.K_SPACE]:
            # Pokeball time!
            self.charge_pokeball()
            target_direction = self.get_target_direction()
            self.throw_preview_points = get_pokeball_trajectory(
                self.x,
                self.y,
                target_direction,
                self.throw_charge,
                keys,
                update_context.map_size,
                update_context.pokemon,
            )
            self.render_throw_power = self.throw_charge
        else:
            # Need to check if we can now throw a ball
            pokeball = self.throw_pokeball()

        super().update_intended(update_context)
        return pokeball

    def get_target_direction(self):
        if not self.target:
            return self.facing

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        return normalise_vector((dx, dy))

    def charge_pokeball(self):
        if not self.throwing:
            self.throwing = True
        self.throw_charge += 1

    def throw_pokeball(self):
        if not self.throwing:
            return

        power = self.throw_charge

        direction = self.get_target_direction()
        pokeball = Pokeball(self.x, self.y, direction, throw_power=power)

        self.throwing = False
        self.throw_charge = 0
        return pokeball


def get_player_sprite_info() -> SpriteInfo:
    return SpriteInfo(relative_path=Path("entities/ditto.png"))

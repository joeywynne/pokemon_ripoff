from pathlib import Path
from src.entities.entity import Entity, SpriteInfo
from src.core.settings import PLAYER_SIZE, NPC_SPEED, BLUE_GREEN, TILE_SIZE
import random
from src.movement.behaviour import (
    MovementBehaviour,
    StationaryBehaviour,
    PacingBehaviour,
    WanderBehaviour,
)


class NPC(Entity):
    def __init__(
        self, x: int, y: int, colour: tuple, movement_controller: MovementBehaviour
    ):
        super().__init__(x, y, colour, movement_controller=movement_controller)
        self.size = PLAYER_SIZE
        self.speed = NPC_SPEED
        self.movement_controller: MovementBehaviour = movement_controller

    def set_movement_behavior(self, movement_controller: MovementBehaviour):
        self.movement_controller = movement_controller


class Drowzee(NPC):

    def __init__(
        self, x: int, y: int, colour: tuple, movement_controller: MovementBehaviour
        ):
        super().__init__(x, y, colour, movement_controller=movement_controller)
        self.mass = 2.0

    def get_sprite_info(self) -> SpriteInfo:
        return SpriteInfo(relative_path=Path("entities/drowzee.png"))


def generate_npcs(num_npcs: int, map_width: int, map_height: int) -> list[NPC]:
    return [
        Drowzee(
            random.randint(TILE_SIZE, map_width - TILE_SIZE),
            random.randint(TILE_SIZE, map_height - TILE_SIZE),
            BLUE_GREEN,
            movement_controller=random.choice(
                [
                    StationaryBehaviour(),
                    PacingBehaviour(axis="horizontal"),
                    PacingBehaviour(axis="vertical"),
                    WanderBehaviour(),
                ]
            ),
        )
        for i in range(num_npcs)
    ]

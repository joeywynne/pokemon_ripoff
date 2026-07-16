from pathlib import Path

from src.contracts import EntityPositionProtocol, UpdateContext
from src.entities.entity import Entity, SpriteInfo
from src.behaviours.behaviour import PokeballBehaviour
from src.core.settings import POKEBALL_SIZE


class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Projectile(Entity):
    pass


class Pokeball(Projectile):
    def __init__(self, x, y, facing: tuple = (1, 0), throw_power: float = 5.0):
        super().__init__(
            x,
            y,
            POKEBALL_SIZE,
            0.5,
            1.0,
            get_pokeball_sprite_info(),
            movement_controller=PokeballBehaviour(
                facing=facing, throw_power=throw_power
            ),
        )
        self.size = POKEBALL_SIZE
        self.mass = 0.5
        self.start_deactivating = False
        self.active_timer = 25
        self.squash_timer = 0.0
        self.ball_value = 255  # Default value for a standard Pokeball


def get_pokeball_sprite_info() -> SpriteInfo:
    return SpriteInfo(
        relative_path=Path("entities/pokeballs.png"),
        position=(20, 20),
        sprite_size=(120, 120),
    )


def get_pokeball_trajectory(
    start_x,
    start_y,
    direction,
    throw_power,
    keys,
    map_size,
    nearby_entities: list[EntityPositionProtocol],
):
    simulation_ball = Pokeball(start_x, start_y, direction, throw_power)
    simulation_context = UpdateContext(
        player_position=Position(start_x, start_y),
        map_size=map_size,
        keys=keys,
        nearby_entities=nearby_entities,
    )

    simulation = PokeballBehaviour(direction, throw_power)
    points = []
    for _ in range(0, 100):  # Simulate for 100 frames
        dx, dy = simulation.get_intended_move(simulation_ball, simulation_context)
        start_x += dx
        start_y += dy
        points.append((start_x, start_y))
    return points

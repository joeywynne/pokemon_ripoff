from pathlib import Path

from src.entities.entity import Entity, SpriteInfo
from src.behaviours.behaviour import PokeballBehaviour
from src.core.settings import POKEBALL_SIZE
from src.entities.pokemon import Pokemon


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

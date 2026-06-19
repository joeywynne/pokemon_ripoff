from src.entities.entity import Entity
from src.movement.behaviour import PokeballBehaviour
from src.core.settings import POKEBALL_SIZE
from typing import Optional


class Projectile(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)

    def update(self, **kwargs) -> Optional[Entity]:
        if self.z < 0.1 and self.vz < 0.1:
            self.is_active = False  # Signal that this projectile should be removed
        return super().update(**kwargs)


class Pokeball(Projectile):
    def __init__(self, x, y, colour, facing: tuple = (1, 0), throw_power: float = 5.0):
        super().__init__(x, y, colour)
        self.size = POKEBALL_SIZE
        self.mass = 0.5
        self.movement_controller = PokeballBehaviour(
            facing=facing, throw_power=throw_power
        )

from src.entities.entity import Entity, SpriteInfo
from pathlib import Path
from src.core.settings import POKEBALL_SIZE


class Projectile(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)


class Pokeball(Projectile):
    def __init__(self, x, y, colour, direction: tuple = (1, 0), throw_power: float = 5.0):
        super().__init__(x, y, colour)
        self.size = POKEBALL_SIZE
        self.speed = 5.0
        self.mass = 0.5

        # Compute an initial velocity from facing direction and throw power.
        clamped_power = max(1.0, min(throw_power, 60.0))
        magnitude = min(40.0, self.speed * (1.0 + clamped_power / 10.0))
        self._velocity = (direction[0] * magnitude, direction[1] * magnitude)

        pokeball_info = SpriteInfo(
            relative_path=Path("entities/pokeballs.png"),
            position=(0, 0),
            sheet_size=(5, 5),
        )
        self.sprite_info = pokeball_info

    def get_intended_move(self, **kwargs) -> tuple[float, float]:
        # Pokeball moves along its computed velocity each frame.
        return self._velocity

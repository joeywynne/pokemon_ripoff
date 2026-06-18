from src.core import settings
from src.entities.entity import Entity, SpriteInfo
from pathlib import Path
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

        # Compute an initial velocity from facing direction and throw power.
        clamped_power = max(1.0, min(throw_power, 60.0))
        base_speed = 5.0
        magnitude = min(40.0, 1.0 + clamped_power / 10.0) * base_speed
        self._velocity = (facing[0] * magnitude, facing[1] * magnitude)
        self.vz = magnitude * 0.75

        pokeball_info = SpriteInfo(
            relative_path=Path("entities/pokeballs.png"),
            position=(0, 0),
            sheet_size=(5, 5),
        )
        self.sprite_info = pokeball_info

    def get_intended_move(self, **kwargs) -> tuple[float, float]:
        # Return the intended move based on current velocity
        self.vz -= settings.GRAVITY  # Simulate gravity effect on vertical velocity
        self.z += self.vz  # Update vertical position
        if self.z < 0:
            self.z = 0
            self.vz = -self.vz * 0.5  # Bounce effect with energy loss
            
            if self.vz < 0.25:  # If the vertical velocity is very small, stop bouncing
                self.vz = 0

        # dampen velocity
        self._velocity = (self._velocity[0] * 0.98, self._velocity[1] * 0.98)
        return self._velocity

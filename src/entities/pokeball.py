from src.entities.entity import Entity, SpriteInfo
from pathlib import Path
from src.core.settings import POKEBALL_SIZE


class Projectile(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)


class Pokeball(Projectile):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
        self.size = POKEBALL_SIZE
        self.speed = 5
        self.mass = 0.5

        pokeball_info = SpriteInfo(
            relative_path=Path("entities/pokeballs.png"),
            position=(0, 0),
            sheet_size=(5, 5),
        )
        self.sprite_info = pokeball_info

from src.entities.entity import Entity


class Projectile(Entity):
    pass

class Pokeball(Projectile):
    def __init__(self, x, y, colour):
        super().__init__(self, x, y, colour, speed)
        self.size = POKEBALL_SIZE
        self.speed = speed
        self.sprite: Optional[str] = "entities/ditto.png"
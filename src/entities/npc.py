from src.entities.player import Entity
from src.core.settings import PLAYER_SIZE, NPC_SPEED
import random


class NPC(Entity):
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.colour = colour
        self.size = PLAYER_SIZE
        self.speed = NPC_SPEED

    def update(self):
        "Update the NPC's position."
        direction = int(random.random() * 4)
        if direction == 0:
            self.x += self.speed
        elif direction == 1:
            self.x -= self.speed
        elif direction == 2:
            self.y += self.speed
        else:
            self.y -= self.speed
        
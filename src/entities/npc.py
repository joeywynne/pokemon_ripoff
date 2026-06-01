from typing import Optional
from src.core.map.collision_map import CollisionMap
from src.entities.entity import Entity
from src.core.settings import PLAYER_SIZE, NPC_SPEED, BLUE_GREEN, TILE_SIZE
import random
from enum import Enum


class MovementType(Enum):
    STATIONARY = 0
    PACING_VERTICAL = 1
    PACING_HORIZONTAL = 2
    WANDERING = 3
    # Add move as necessary
    #FOLLOWING = 4


class NPC(Entity):
    def __init__(self, x: int, y: int, colour: tuple, movement_type: MovementType):
        super().__init__(x, y, colour)
        self.size = PLAYER_SIZE
        self.speed = NPC_SPEED
        self.sprite: Optional[str] = "entities/drowzee.png"
        self.movement_type: MovementType = movement_type
        self.mass = 200.0

        self.pace_direction = 1
        self.pace_distance = 180
        self.pace_travelled = 0

        self.wander_timer = 0
        self.wander_direction = (0, 0)
        self.change_direction_interval = random.randint(60, 120)

    def set_movement_type(self, movement_type: MovementType):
        self.movement_type = movement_type

    def get_move(self) -> tuple[float, float]:
        if self.movement_type == MovementType.STATIONARY:
            return 0, 0
        
        elif self.movement_type == MovementType.PACING_VERTICAL:
            return self._pacing(axis=0)

        elif self.movement_type == MovementType.PACING_HORIZONTAL:
            return self._pacing(axis=1)

        elif self.movement_type == MovementType.WANDERING:
            return self._wandering()
        
    def _pacing(self, axis: int) -> tuple[float, float]:
        if axis == 0:
            dx = 0
            dy = self.speed * self.pace_direction
        else:
            dx = self.speed * self.pace_direction
            dy = 0

        self.pace_travelled += abs(dx if axis == 1 else dy)
        if self.pace_travelled >= self.pace_distance:
            self.pace_direction *= -1
            self.pace_travelled = 0

        return dx, dy   
    
    def _wandering(self) -> tuple[float, float]:
        self.wander_timer += 1
        if self.wander_timer >= self.change_direction_interval or self.wander_direction == (0, 0):
            self.wander_timer = 0
            self.change_direction_interval = random.randint(60, 120)
            self.wander_direction = (round(random.uniform(-1, 1)), round(random.uniform(-1, 1)))

        dx = self.speed * self.wander_direction[0]
        dy = self.speed * self.wander_direction[1]
        return dx, dy

def generate_npcs(num_npcs: int, map_width: int, map_height: int) -> list[NPC]:
    return [
        NPC(
            random.randint(TILE_SIZE, map_width - TILE_SIZE),
            random.randint(TILE_SIZE, map_height - TILE_SIZE),
            BLUE_GREEN,
            list(MovementType)[i]
        ) for i in range(num_npcs)
    ]

from dataclasses import dataclass
import uuid
import pygame
from typing import Optional
from pathlib import Path
from src.behaviours.behaviour import MovementBehaviour
from src.contracts import EntityPositionProtocol
from src.behaviours.targeting_system import TargetingProtocol
from src.utils import normalise_vector

@dataclass
class SpriteInfo:
    relative_path: Path
    position: Optional[tuple] = None
    sprite_size: Optional[tuple] = None


class Entity:
    def __init__(
        self,
        x: float,
        y: float,
        size: float,
        mass: float,
        speed: float,
        sprite_info: SpriteInfo,
        movement_controller: MovementBehaviour,
        targeting_system: TargetingProtocol | None = None,
    ):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.z = 0
        self.size = size
        self.mass = mass
        self.speed = speed
        self.sprite_info = sprite_info
        self.velocity = [0.0, 0.0]
        self.desired_velocity = [0.0, 0.0]
        self.facing = (1, 0)
        self.rotation = 0.0
        self.is_active = True
        self.movement_controller = movement_controller
        self.targeting_system = targeting_system
        self.target: Optional[EntityPositionProtocol] | None = None

    @property
    def momentum(self) -> tuple[float, float]:
        return self.mass * self.velocity[0], self.mass * self.velocity[1]

    @property
    def desired_momentum(self) -> tuple[float, float]:
        return (
            self.mass * self.desired_velocity[0],
            self.mass * self.desired_velocity[1],
        )

    def get_sprite_info(self) -> SpriteInfo:
        return self.sprite_info

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_intended_move(self, update_context) -> tuple[float, float]:
        return self.movement_controller.get_intended_move(self, update_context)

    def update_intended(self, update_context) -> None:
        intended_move = self.get_intended_move(update_context)
        dx, dy = intended_move

        if dx != 0 and dy != 0:
            dx *= 0.7071  # ≈ 1/sqrt(2)
            dy *= 0.7071

        self.desired_velocity = [dx, dy]
        self.target = self.get_target(update_context)

    def get_target(self, update_context) -> Optional[EntityPositionProtocol]:
        if self.targeting_system:
            return self.targeting_system.get_target(self, update_context.nearby_entities)
    
    def get_target_direction(self):
        if not self.target:
            return self.facing

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        return normalise_vector((dx, dy))

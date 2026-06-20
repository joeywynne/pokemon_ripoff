from dataclasses import dataclass
import pygame
from typing import Optional
from pathlib import Path
from src.movement.behaviour import MovementBehaviour


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
    ):
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

    def get_intended_move(self, **kwargs) -> tuple[float, float]:
        return self.movement_controller.get_intended_move(self, **kwargs)

    def update_intended(self, **kwargs) -> None:
        intended_move = self.get_intended_move(**kwargs)
        dx, dy = intended_move

        if dx != 0 and dy != 0:
            dx *= 0.7071  # ≈ 1/sqrt(2)
            dy *= 0.7071

        self.desired_velocity = [dx, dy]

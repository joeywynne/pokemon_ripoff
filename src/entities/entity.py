from dataclasses import dataclass
import pygame
from src.core.map.collision_map import CollisionMap
from typing import Optional
from pathlib import Path


@dataclass
class SpriteInfo:
    relative_path: Path
    position: Optional[tuple] = None
    sheet_size: Optional[tuple] = None


class Entity:
    def __init__(self, x: float, y: float, colour: tuple):
        self.x = x
        self.y = y
        self.velocity = [0.0, 0.0]
        self.desired_velocity = [0.0, 0.0]
        self.mass = 1.0
        self.colour = colour
        self.sprite_info: Optional[SpriteInfo] = None

    @property
    def momentum(self) -> tuple[float, float]:
        return self.mass * self.velocity[0], self.mass * self.velocity[1]

    @property
    def desired_momentum(self) -> tuple[float, float]:
        return (
            self.mass * self.desired_velocity[0],
            self.mass * self.desired_velocity[1],
        )

    @property
    def facing(self) -> tuple[int, int]:
        # Determine facing direction based on velocity
        if self.velocity[0] > 0:
            return (1, 0)  # Facing right
        elif self.velocity[0] < 0:
            return (-1, 0)  # Facing left
        else:
            return (1, 0)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_intended_move(self, **kwargs) -> tuple[float, float]:
        # Default to no movement
        return 0, 0

    def update(self, **kwargs) -> Optional[Entity]:
        intended_move = self.get_intended_move(**kwargs)
        new_entity = None
        if len(intended_move) == 3:
            dx, dy, new_entity = intended_move
        else:
            dx, dy = intended_move

        if dx != 0 and dy != 0:
            dx *= 0.7071  # ≈ 1/sqrt(2)
            dy *= 0.7071

        self.desired_velocity = [dx, dy]
        return new_entity

    def _apply_desired_move(self, collision_map: CollisionMap):
        dx, dy = self.desired_velocity
        if dx != 0:
            target_x = self.x + dx
            target_rect = pygame.Rect(target_x, self.y, self.size, self.size)
            if can_move_to(target_rect, collision_map):
                self.x = target_x
                self.desired_velocity[0] = dx
        else:
            self.desired_velocity[0] = 0

        if dy != 0:
            target_y = self.y + dy
            target_rect = pygame.Rect(self.x, target_y, self.size, self.size)
            if can_move_to(target_rect, collision_map):
                self.y = target_y
        else:
            self.desired_velocity[1] = 0

    def _final_safety(self, collision_map: CollisionMap):
        """Emergency correction if entity ends up in invalid position."""
        if not can_move_to(self.get_rect(), collision_map):
            # Push back along last movement
            self.x -= self.desired_velocity[0] * 2.5
            self.y -= self.desired_velocity[1] * 2.5

            # Last resort: snap to integer position
            if not can_move_to(self.get_rect(), collision_map):
                self.x = round(self.x)
                self.y = round(self.y)
                self.desired_velocity = [0.0, 0.0]

        self.velocity = self.desired_velocity


def can_move_to(target_rect: pygame.Rect, collision_map: CollisionMap) -> bool:
    return not collision_map.collides(target_rect)


def entities_collide(a: Entity, b: Entity) -> bool:
    """Check if two entities are overlapping"""
    return a.get_rect().colliderect(b.get_rect())

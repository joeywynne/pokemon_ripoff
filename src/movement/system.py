import pygame
from src.core.map.collision_map import CollisionMap


class MovementSystem:

    @staticmethod
    def move_entity(entity, collision_map: CollisionMap):
        dx, dy = entity.desired_velocity
        actual_dx = 0
        actual_dy = 0

        if dx != 0:
            target_rect = entity.get_rect().move(dx, 0)
            if can_move_to(target_rect, collision_map):
                entity.x += dx
                actual_dx = dx

        if dy != 0:
            target_rect = entity.get_rect().move(0, dy)
            if can_move_to(target_rect, collision_map):
                entity.y += dy
                actual_dy = dy

        entity.desired_velocity = [actual_dx, actual_dy]

        MovementSystem.update_facing(entity)

    @staticmethod
    def update_facing(entity):
        """Update the facing direction of the entity based on its desired velocity."""
        if entity.desired_velocity != [0.0, 0.0]:
            entity.facing = normalise_vector(entity.desired_velocity)

    @staticmethod
    def final_safety(entity, collision_map: CollisionMap):
        """Ensure the entity is not stuck in a wall after movement."""
        if not can_move_to(entity.get_rect(), collision_map):
            # Push back along last movement
            entity.x -= entity.desired_velocity[0] * 2.5
            entity.y -= entity.desired_velocity[1] * 2.5

            # Last resort: snap to integer position
            if not can_move_to(entity.get_rect(), collision_map):
                entity.x = round(entity.x)
                entity.y = round(entity.y)
                entity.desired_velocity = [0.0, 0.0]

        entity.velocity = entity.desired_velocity


def can_move_to(target_rect: pygame.Rect, collision_map: CollisionMap) -> bool:
    return not collision_map.collides(target_rect)


def normalise_vector(vector: tuple[float, float]) -> tuple[float, float]:
    """Return a normalized version of the vector."""
    x, y = vector
    magnitude = (x**2 + y**2) ** 0.5
    if magnitude == 0:
        return (0, 0)
    return (x / magnitude, y / magnitude)

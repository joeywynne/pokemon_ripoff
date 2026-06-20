from src.entities.entity import Entity
from src.core.map.collision_map import CollisionMap
import pygame


def move_entities(entities: list[Entity], collision_map: CollisionMap) -> list[Entity]:
    """Move all entities based on their desired moves and resolve collisions."""
    # Each entity now has a desired velocity.
    # Use this to try and move them and then resolve any issues with collisions.
    for entity in entities:
        move_entity(entity, collision_map)

    resolve_all_collisions(entities, collision_map)

    for entity in entities:
        final_safety(entity, collision_map)

    entities[:] = [entity for entity in entities if entity.is_active]


def move_entity(entity, collision_map: CollisionMap):
    """Move an entity based on its desired velocity

    This function checks for collisions with the collision map and adjusts the entity's position accordingly.
    """
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

    if entity.desired_velocity != [0.0, 0.0]:
        entity.facing = normalise_vector(entity.desired_velocity)


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


def resolve_all_collisions(entities: list[Entity], collision_map: CollisionMap):
    """Resolve all collisions using the desired move of the entities.

    Order:
      1. Apply movement + tile collision for everyone
      2. Resolve entity vs entity collisions
      3. Final safety check
    """

    for _ in range(5):  # Multiple passes to resolve entity collisions
        any_collisions_resolved = False

        # Check each pair of entities for collision
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                a = entities[i]
                b = entities[j]

                if entities_collide(a, b) and abs(a.z - b.z) < 5.0:
                    resolve_entity_collision(a, b)
                    any_collisions_resolved = True

        # No more collisions, we can stop early
        if not any_collisions_resolved:
            break


def resolve_entity_collision(a: Entity, b: Entity):
    """Use momentum to push two colliding entities apart."""
    # Calculate the direction from a to b
    dx = b.x - a.x
    dy = b.y - a.y
    dist = (dx**2 + dy**2) ** 0.5 + 0.001  # Avoid division by zero

    # Normal vector
    nx = dx / dist
    ny = dy / dist

    # Overlap
    overlap = (a.size + b.size) / 2 - dist + 1.0  # Give a small buffer
    if overlap <= 0:
        return

    total_mass = a.mass + b.mass
    a_push = b.mass / total_mass
    b_push = a.mass / total_mass
    push_distance = overlap * 0.65

    # Apply the push
    a.x -= nx * push_distance * a_push
    a.y -= ny * push_distance * a_push
    b.x += nx * push_distance * b_push
    b.y += ny * push_distance * b_push


def entities_collide(a: Entity, b: Entity) -> bool:
    """Check if two entities are overlapping"""
    return a.get_rect().colliderect(b.get_rect())

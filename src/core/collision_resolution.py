from src.entities.entity import Entity, entities_collide
from src.core.map.collision_map import CollisionMap


def resolve_all_collisions(entities: list[Entity], collision_map: CollisionMap):
    """Resolve all collisions using the desired move of the entities.
    
    Order:
      1. Apply movement + tile collision for everyone
      2. Resolve entity vs entity collisions
      3. Final safety check
    """
    # Try to apply the moves
    for entity in entities:
        entity._apply_desired_move(collision_map)
    
    for _ in range(5):  # Multiple passes to resolve entity collisions
        any_collisions_resolved = False
        
        # Check each pair of entities for collision
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                a = entities[i]
                b = entities[j]
                
                if entities_collide(a, b):
                    _resolve_entity_collision(a, b)
                    any_collisions_resolved = True

        # No more collisions, we can stop early
        if not any_collisions_resolved:
            break

        # Run the final safety checks for our entities
        for entity in entities:
            entity._final_safety(collision_map)

def _resolve_entity_collision(a: Entity, b: Entity):
    """Use momentum to push two colliding entities apart."""
    # Calculate the direction from a to b
    dx = b.x - a.x
    dy = b.y - a.y
    dist = (dx**2 + dy**2) ** 0.5 + 0.001  # Avoid division by zero

    # Normal vector
    nx = dx / dist
    ny = dy / dist

    # Overlap
    overlap = (a.size + b.size) / 2 - dist + 1.0 # Give a small buffer
    if overlap <= 0:
        return

    total_mass = a.mass + b.mass
    a_push = (b.mass / total_mass)
    b_push = (a.mass / total_mass)
    push_distance = overlap * 0.65

    # Apply the push
    a.x -= nx * push_distance * a_push
    a.y -= ny * push_distance * a_push
    b.x += nx * push_distance * b_push
    b.y += ny * push_distance * b_push


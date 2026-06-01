import pygame
from src.core.map.collision_map import CollisionMap
from typing import Optional

class Entity:
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.mass = 1
        self.colour = colour
        self.sprite: Optional[str] = None

    @property
    def momentum(self) -> tuple[float, float]:
        print("mass:", self.mass)
        print("velocity:", self.velocity)
        return self.mass * self.velocity[0], self.mass * self.velocity[1]

    @property
    def facing(self) -> tuple[int, int]:
        # Determine facing direction based on velocity
        if self.velocity[0] > 0:
            return (1, 0)  # Facing right
        elif self.velocity[0] < 0:
            return (-1, 0) # Facing left
        else:
            return (1, 0)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def get_move(self, **kwargs) -> tuple[float, float]:
        # Default to no movement
        return 0, 0
    
    def update(self, collision_map: CollisionMap, entities: list[Entity], **kwargs):
        dx, dy = self.get_move(**kwargs)
        
        if dx != 0 and dy != 0:
            dx *= 0.7071   # ≈ 1/sqrt(2)
            dy *= 0.7071
        
        self._resolve_target_pos(dx, dy, collision_map)
        self._resolve_entity_collisions(entities, collision_map)

    def _resolve_target_pos(self, dx: float, dy: float, collision_map: CollisionMap):
        if dx != 0:
            target_x = self.x + dx
            target_rect = pygame.Rect(target_x, self.y, self.size, self.size)
            if can_move_to(target_rect, collision_map):
                self.x = target_x
                self.velocity[0] = dx
        else:
            self.velocity[0] = 0

        if dy != 0:
            target_y = self.y + dy
            target_rect = pygame.Rect(self.x, target_y, self.size, self.size)
            if can_move_to(target_rect, collision_map):
                self.y = target_y
                self.velocity[1] = dy
        else:
            self.velocity[1] = 0

    def _resolve_entity_collisions(self, entities: list[Entity], collision_map: CollisionMap):
        # This is close but a light player can still push against a heavy npc
        for other in entities:
            if other is self or not entities_collide(self, other):
                continue

            total_mass = self.mass + other.mass
            entity_momentum = self.momentum
            other_momentum = other.momentum
            nx = (entity_momentum[0] + other_momentum[0]) / total_mass
            ny = (entity_momentum[1] + other_momentum[1]) / total_mass
            print("entity momenta:", self.momentum)
            print("other momenta:", other.momentum)
            
            # resolve overlap
            overlap_x = (self.size + other.size) / 2 - abs(self.x + nx - other.x)
            overlap_y = (self.size + other.size) / 2 - abs(self.y + ny - other.y)

            dx, dy = 0, 0
            if overlap_x < overlap_y:          # Push horizontally
                if self.x < other.x:
                    dx = nx + (-overlap_x * 0.5)
                else:
                    dx = nx + (overlap_x * 0.5) 
            else:                              # Push vertically
                if self.y < other.y:
                    dy = ny + (-overlap_y * 0.5)
                else:
                    dy = ny + (overlap_y * 0.5)

            self._resolve_target_pos(dx, dy, collision_map)



def can_move_to(target_rect: pygame.Rect, collision_map: CollisionMap) -> bool:
    return not collision_map.collides(target_rect)


def entities_collide(a: Entity, b: Entity) -> bool:
    """Check if two entities are overlapping"""
    return a.get_rect().colliderect(b.get_rect())

from math import atan2, radians
from src.contracts import EntityPositionProtocol
from typing import Protocol


class TargetingProtocol(Protocol):

    def get_target(self, entity, nearby_entities) -> EntityPositionProtocol | None: ...


class VisionTargeting:

    def get_target(self, entity, nearby_entities) -> EntityPositionProtocol | None:
        """Find the closest Pokemon to the entity within the entity's cone of vision."""
        closest_pokemon = None
        closest_distance = float("inf")
        for nearby_entity in nearby_entities:
            if nearby_entity.id == entity.id:
                continue
            if self._is_in_angle_of_vision(entity, nearby_entity):
                distance = get_distance(entity.x, entity.y, nearby_entity)
                if distance <= entity.vision_distance and distance < closest_distance:
                    closest_distance = distance
                    closest_pokemon = nearby_entity
        return closest_pokemon

    def _is_in_angle_of_vision(self, entity, pokemon: EntityPositionProtocol) -> bool:
        """Check if a Pokemon is within the player's cone of vision."""
        dy = pokemon.y - entity.y
        dx = pokemon.x - entity.x
        angle_to_pokemon = atan2(dy, dx)
        facing = entity.facing
        facing_angle = atan2(facing[1], facing[0])
        vision_radians = radians(entity.vision_angle)
        return (
            facing_angle - vision_radians
            <= angle_to_pokemon
            <= facing_angle + vision_radians
        )


class NearestTargeting:
    def __init__(self, start_targeting_distance: float, stop_targeting_distance: float):
        self.start_targeting_distance = start_targeting_distance
        self.stop_targeting_distance = stop_targeting_distance
        self.current_target: EntityPositionProtocol | None = None

    def get_target(self, entity, nearby_entities) -> EntityPositionProtocol | None:
        if self.current_target is not None:
            distance = get_distance(entity.x, entity.y, self.current_target)
            if distance > self.stop_targeting_distance:
                self.current_target = None
            else:
                return self.current_target

        # Find the closest entity.
        closest_entity = None
        closest_distance = float("inf")
        for nearby_entity in nearby_entities:
            if nearby_entity.id == entity.id:
                continue  # Skip self
            distance = get_distance(entity.x, entity.y, nearby_entity)
            if distance < closest_distance and distance <= self.start_targeting_distance:
                closest_entity = nearby_entity
                closest_distance = distance
        self.current_target = closest_entity
        return self.current_target


def get_distance(player_x, player_y, entity: EntityPositionProtocol) -> float:
    return ((player_x - entity.x) ** 2 + (player_y - entity.y) ** 2) ** 0.5

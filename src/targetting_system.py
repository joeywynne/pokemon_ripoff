from src.entities.pokeball import Pokeball
from src.entities.pokemon import Pokemon
from src.movement.behaviour import PokeballBehaviour
from typing import Optional
from src.entities.entity import Entity
from math import atan2, radians
from src.core.utils import UpdateContext


def find_target(
    player_x, player_y, facing, vision_angle, vision_distance, pokemon: list[Pokemon]
) -> Optional[Pokemon]:
    """Find the closest Pokemon to the player within the player's cone of vision."""
    closest_pokemon = None
    closest_distance = float("inf")
    for p in pokemon:
        if is_in_angle_of_vision(player_x, player_y, facing, vision_angle, p):
            distance = get_distance(player_x, player_y, p)
            if distance <= vision_distance and distance < closest_distance:
                closest_distance = distance
                closest_pokemon = p
    return closest_pokemon


def get_distance(player_x, player_y, entity: Entity) -> float:
    return ((player_x - entity.x) ** 2 + (player_y - entity.y) ** 2) ** 0.5


def is_in_angle_of_vision(
    player_x, player_y, facing, vision_angle, pokemon: Pokemon
) -> bool:
    """Check if a Pokemon is within the player's cone of vision."""
    dy = pokemon.y - player_y
    dx = pokemon.x - player_x
    angle_to_pokemon = atan2(dy, dx)
    facing_angle = atan2(facing[1], facing[0])
    vision_radians = radians(vision_angle)
    return (
        facing_angle - vision_radians
        <= angle_to_pokemon
        <= facing_angle + vision_radians
    )


def get_pokeball_trajectory(
    start_x, start_y, direction, throw_power, keys, map_size, pokemon
):
    simulation_ball = Pokeball(start_x, start_y, direction, throw_power)
    simulation_context = UpdateContext(
        entity=simulation_ball,
        player_position=(start_x, start_y),
        map_size=map_size,
        keys=keys,
        pokemon=pokemon,
    )

    simulation = PokeballBehaviour(direction, throw_power)
    points = []
    for _ in range(0, 100):  # Simulate for 100 frames
        dx, dy = simulation.get_intended_move(simulation_context)
        start_x += dx
        start_y += dy
        points.append((start_x, start_y))
    return points

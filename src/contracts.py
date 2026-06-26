# Neutral module for type definitions which depends on structural types / Protocol shapes
# Not dependant on concrete Classes

from typing import Protocol
from dataclasses import dataclass


class EntityPositionProtocol(Protocol):
    x: float
    y: float


@dataclass
class UpdateContext:
    keys: dict
    nearby_pokemon: list[EntityPositionProtocol]
    player_position: tuple[float, float]
    map_size: tuple[int, int]
    
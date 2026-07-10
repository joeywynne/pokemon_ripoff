# Neutral module for type definitions which depends on structural types / Protocol shapes
# Not dependant on concrete Classes

from typing import Protocol
from dataclasses import dataclass, field


class EntityPositionProtocol(Protocol):
    x: float
    y: float


@dataclass
class UpdateContext:
    keys: dict
    nearby_entities: list[EntityPositionProtocol]
    player_position: tuple[float, float]
    map_size: tuple[int, int]
    event_queue: list = field(default_factory=list)

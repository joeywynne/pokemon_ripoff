from dataclasses import dataclass
from src.entities.entity import Entity
from src.entities.pokemon import Pokemon


@dataclass
class UpdateContext:
    keys: dict
    pokemon: list[Pokemon]
    entity: Entity
    player_position: tuple[float, float]
    map_size: tuple[int, int]

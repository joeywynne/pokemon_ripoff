from enum import Enum
from dataclasses import dataclass
from src.entities.entity import SpriteInfo
from src.movement.behaviour import MovementBehaviour
from src.movement.composite_behaviours import StationaryWanderBehaviour


class PokemonType(Enum):
    GHOST = "ghost"
    PSYCHIC = "psychic"
    FIRE = "fire"
    GRASS = "grass"
    WATER = "water"
    ELECTRIC = "electric"


@dataclass
class PokemonSpecies():
    name: str
    types: list[PokemonType]
    #base_hp: int
    #base_attack: int
    #base_defense: int
    speed: int
    mass: float
    size: int
    behaviour_factory: MovementBehaviour
    sprite_info: SpriteInfo



DROWZEE = PokemonSpecies(
    name="Drowzee",
    types=[PokemonType.PSYCHIC],
    speed=2,
    mass=2.0,
    size=40,
    behaviour_factory=StationaryWanderBehaviour,
    sprite_info=SpriteInfo(relative_path="entities/drowzee.png")
)
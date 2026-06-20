from enum import Enum
from dataclasses import dataclass
from src.entities.entity import SpriteInfo
from src.movement.behaviour import MovementBehaviour
from src.movement.composite_behaviours import (
    StationaryWanderBehaviour,
    StationaryTeleportBehaviour,
    WanderFollowBehaviour,
    WanderFleeBehaviour,
)


class PokemonType(Enum):
    GHOST = "ghost"
    PSYCHIC = "psychic"
    FIRE = "fire"
    GRASS = "grass"
    WATER = "water"
    ELECTRIC = "electric"
    POISON = "poison"


@dataclass
class PokemonSpecies:
    name: str
    types: list[PokemonType]
    # base_hp: int
    # base_attack: int
    # base_defense: int
    speed: int
    mass: float
    size: int
    behaviour_factory: MovementBehaviour
    sprite_info: SpriteInfo


DROWZEE = PokemonSpecies(
    name="Drowzee",
    types=[PokemonType.PSYCHIC],
    speed=1.5,
    mass=2.0,
    size=40,
    behaviour_factory=StationaryWanderBehaviour,
    sprite_info=SpriteInfo(relative_path="entities/drowzee.png"),
)

GHASTLY = PokemonSpecies(
    name="Ghastly",
    types=[PokemonType.GHOST, PokemonType.POISON],
    speed=2,
    mass=0.5,
    size=35,
    behaviour_factory=WanderFollowBehaviour,
    sprite_info=SpriteInfo(relative_path="entities/ghastly.png"),
)

NIDORAN = PokemonSpecies(
    name="Nidoran",
    types=[PokemonType.POISON],
    speed=1.8,
    mass=1.5,
    size=20,
    behaviour_factory=WanderFleeBehaviour,
    sprite_info=SpriteInfo(relative_path="entities/nidoran.png"),
)

ABRA = PokemonSpecies(
    name="Abra",
    types=[PokemonType.PSYCHIC],
    speed=1.8,
    mass=1.5,
    size=36,
    behaviour_factory=StationaryTeleportBehaviour,
    sprite_info=SpriteInfo(relative_path="entities/abra.png"),
)

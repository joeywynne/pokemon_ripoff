from src.entities.entity import Entity
from src.pokemon.base import PokemonSpecies

from src.core.settings import TILE_SIZE
import random
from src.pokemon.base import DROWZEE, GHASTLY, NIDORAN, ABRA


class Pokemon(Entity):

    def __init__(
        self,
        x,
        y,
        species: PokemonSpecies,
    ):
        self.species = species
        super().__init__(
            x,
            y,
            species.size,
            species.mass,
            species.speed,
            species.sprite_info,
            movement_controller=species.behaviour_factory(),
        )


def generate_pokemon(num_pokemon: int, map_width: int, map_height: int) -> list[Entity]:
    return [
        Pokemon(
            random.randint(TILE_SIZE, map_width - TILE_SIZE),
            random.randint(TILE_SIZE, map_height - TILE_SIZE),
            random.choice([DROWZEE, GHASTLY, NIDORAN, ABRA]),
        )
        for _ in range(num_pokemon)
    ]

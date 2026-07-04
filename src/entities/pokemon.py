from enum import Enum

from src.entities.entity import Entity
from src.pokemon.species import PokemonSpecies

from src.core.settings import TILE_SIZE
import random
from src.pokemon.species import DROWZEE, GASTLY, NIDORAN, ABRA
from src.pokemon.catching import attempt_capture
from src.behaviours.behaviour import FleeBehaviour, FollowBehaviour
from src.behaviours.behaviour_registry import BEHAVIOUR_FACTORIES


class PokemonState(Enum):
    HEALTHY = "healthy"
    POISONED = "poisoned"
    BURNED = "burned"
    PARALYSED = "paralysed"
    FROZEN = "frozen"
    ASLEEP = "asleep"


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
            movement_controller=BEHAVIOUR_FACTORIES[species.behaviour_id](),
        )
        self.hp = species.base_hp
        self.status = PokemonState.HEALTHY
        self.is_captured = False
        self.name = self.species.name
        self.is_buddy = False

    @property
    def statusCondition(self) -> str:
        if self.status in [
            PokemonState.POISONED,
            PokemonState.PARALYSED,
            PokemonState.BURNED,
        ]:
            return 12
        elif self.status in [PokemonState.FROZEN, PokemonState.ASLEEP]:
            return 25
        else:
            return 0

    def get_approx_catch_probability(self, ball_value: int = 255) -> float:
        """
        Calculate the probability of catching this Pokemon based on its current HP and the type of Pokeball used.
        The formula is based on the catch rate and the current HP of the Pokemon.
        https://bulbapedia.bulbagarden.net/wiki/Catch_rate#Approximate_probability
        """
        status_prior = self.statusCondition / (ball_value + 1)

        ball = 8 if ball_value == 200 else 12
        if self.hp <= 0:
            f = 255
        else:
            f = (self.species.base_hp * 255 * 4) / (self.hp * ball)
        f = min(f, 255)
        f = max(f, 1)

        catch_term = (self.species.catch_rate + 1) / (ball_value + 1)
        f_term = (f + 1) / 256
        return status_prior + (catch_term * f_term)

    def on_hit_by_pokeball(self, pokeball):
        result = attempt_capture(pokemon=self, pokeball=pokeball)
        result = True

        if result:
            self.on_capture()
        else:
            self.on_capture_failure()

    def on_capture(self):
        self.movement_controller = FollowBehaviour(
            previous_behaviour=self.movement_controller,
            speed_multiplier=3.0,
            min_distance=0.0,
        )
        self.is_captured = True

    def on_capture_failure(self):
        self.movement_controller = FleeBehaviour(
            previous_behaviour=self.movement_controller,
            speed_multiplier=3.0,
            duration=300,
        )


def generate_pokemon(
    num_pokemon: int, map_width: int, map_height: int
) -> list[Pokemon]:
    return [
        Pokemon(
            random.randint(TILE_SIZE, map_width - TILE_SIZE),
            random.randint(TILE_SIZE, map_height - TILE_SIZE),
            random.choice([DROWZEE, GASTLY, NIDORAN, ABRA]),
        )
        for _ in range(num_pokemon)
    ]

from src.entities.pokemon import Pokemon
from dataclasses import dataclass, field

from src.pokemon.registry import ALL_SPECIES


@dataclass
class GameState:

    party: list[Pokemon] = field(default_factory=list)
    pokedex: dict[str, bool] = field(default_factory=dict)
    # items: list[Items] = field(default_factory=list)

    @classmethod
    def new_game(cls):
        return cls(pokedex={species.name: False for species in ALL_SPECIES})

    @property
    def party_size(self) -> int:
        return len(self.party)

    @property
    def captured_pokemon_count(self) -> int:
        return sum(1 for captured in self.pokedex.values() if captured)

    @property
    def remaining_pokemon_to_catch(self) -> int:
        return sum(1 for captured in self.pokedex.values() if not captured)

    def add_pokemon_to_party(self, pokemon: Pokemon) -> None:
        self.party.append(pokemon)
        self.pokedex[pokemon.name] = True

    def remove_pokemon_from_party(self, pokemon: Pokemon) -> None:
        self.party.remove(pokemon)

from src.entities.pokemon import Pokemon
from src.behaviours.behaviour import BuddyBehaviour
from dataclasses import dataclass, field

from src.pokemon.registry import ALL_SPECIES


@dataclass
class GameState:

    party: list[Pokemon] = field(default_factory=list)
    pokedex: dict[str, bool] = field(default_factory=dict)
    buddy_index: int = -1
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
        self.pokedex[pokemon.species.name] = True

    def remove_pokemon_from_party(self, pokemon: Pokemon) -> None:
        self.party.remove(pokemon)

    def swap_buddy(self, buddy_index: int, pos_x: float, pos_y: float):
        if self.buddy_index == buddy_index:
            return

        # Deactivate previous pokemon
        prev_buddy = try_get_pokemon(self.party, self.buddy_index)
        if prev_buddy:
            prev_buddy.is_active = False
            prev_buddy.is_buddy = False

        self.buddy_index = buddy_index
        if buddy_index == -1:
            return

        # Create and set pokemon
        new_buddy = try_get_pokemon(self.party, buddy_index)
        new_buddy.is_buddy = True
        new_buddy.is_captured = False
        new_buddy.is_active = True
        new_buddy.x = pos_x
        new_buddy.y = pos_y
        new_buddy.movement_controller = BuddyBehaviour()
        return new_buddy


def try_get_pokemon(party, index):
    if 0 <= index < len(party):
        return party[index]

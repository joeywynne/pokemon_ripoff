
from src.core.game_state import GameState
from src.entities.entity import Entity
from src.entities.player import Player
from src.entities.pokemon import Pokemon
from src.entities.pokeball import Pokeball


def process_interaction(
    a: Entity,
    b: Entity,
    game_state: GameState,
):
    
    if isinstance(a, Pokeball) and isinstance(b, Pokemon):
        process_pokeball_hit(a, b)
    
    elif isinstance(b, Pokeball) and isinstance(a, Pokemon):
        process_pokeball_hit(b, a)

    elif isinstance(a, Player) and isinstance(b, Pokemon):
        process_player_pokemon_interaction(b, game_state)

    elif isinstance(b, Player) and isinstance(a, Pokemon):
        process_player_pokemon_interaction(a, game_state)


def process_pokeball_hit(pokeball: Pokeball, pokemon: Pokemon):
    """Process the interaction when a Pokeball hits a Pokemon."""
    pokemon.on_hit_by_pokeball(pokeball)
    # Start the Pokeball deactivation
    pokeball.start_deactivating = True


def process_player_pokemon_interaction(pokemon: Pokemon, game_state: GameState):
    if pokemon.is_captured:
        pokemon.is_active = False
    game_state.add_pokemon_to_party(pokemon)
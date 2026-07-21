from src.core.game_state import GameState
from src.entities.entity import Entity
from src.entities.player import Player
from src.entities.pokemon import Pokemon
from src.entities.pokeball import Pokeball
from src.pokemon.catching import attempt_capture
from src.behaviours.behaviour import FollowBehaviour, FleeBehaviour, TemporaryBehaviour, EntityTargetingSystem


def process_interaction(
    a: Entity,
    b: Entity,
    player: Player,
    game_state: GameState,
):

    if isinstance(a, Pokeball) and isinstance(b, Pokemon):
        process_pokeball_hit(a, b, player)

    elif isinstance(b, Pokeball) and isinstance(a, Pokemon):
        process_pokeball_hit(b, a, player)

    elif isinstance(a, Player) and isinstance(b, Pokemon):
        process_player_pokemon_interaction(b, game_state)

    elif isinstance(b, Player) and isinstance(a, Pokemon):
        process_player_pokemon_interaction(a, game_state)


def process_pokeball_hit(pokeball: Pokeball, pokemon: Pokemon, player: Player):
    """Process the interaction when a Pokeball hits a Pokemon."""
    if pokemon.is_buddy or pokeball.start_deactivating:
        return
    pokeball.start_deactivating = True
    caught = attempt_capture(pokemon, pokeball)
    if caught:
        pokemon.mark_captured()
        follow = FollowBehaviour(
            speed_multiplier=5.0,
            min_distance=0.0,
            targeting_system=EntityTargetingSystem(target=player)
        )
        pokemon.movement_controller = follow
    else:
        temp_flee = TemporaryBehaviour(
            behaviour=FleeBehaviour(
                speed_multiplier=5.0,
                targeting_system=EntityTargetingSystem(target=player)
            ),
            fallback=pokemon.movement_controller,
            duration=300,
        )
        pokemon.movement_controller = temp_flee


def process_player_pokemon_interaction(pokemon: Pokemon, game_state: GameState):
    if pokemon.is_captured:
        pokemon.is_active = False
        pokemon.reset_stats_when_captured()
        game_state.add_pokemon_to_party(pokemon)

import random


def attempt_capture(pokemon, pokeball) -> bool:
    """
    Attempt to catch a Pokemon using a Pokeball.
    Returns True if the Pokemon is caught, False otherwise.
    """
    catch_probability = pokemon.get_approx_catch_probability(
        ball_value=pokeball.ball_value
    )
    random_value = random.random()  # Random float between 0.0 and 1.0
    return random_value < catch_probability

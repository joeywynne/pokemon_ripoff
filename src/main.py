import argparse
import logging

from src.core.game import Game
from src.core.map.tile_map import generate_random_map
from src.core.map.collision_map import generate_collision_map


def setup_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Pokemon Ripoff game.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging and FPS display")
    args = parser.parse_args()

    setup_logging(args.debug)
    probs = {5: 0.5, 1: 0.3, 2: 0.15, 3: 0.05}
    tile_map = generate_random_map(64, 64, probs)
    collision_map = generate_collision_map(tile_map)
    game = Game(tile_map, collision_map,debug=args.debug)
    game.run()


if __name__ == "__main__":
    main()

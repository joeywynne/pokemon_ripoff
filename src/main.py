from src.core.game import Game
from src.core.map.map import generate_random_map

def main():
    probs = {0: 0.5, 1: 0.3, 2: 0.15, 3: 0.05}
    tile_map = generate_random_map(64, 64, probs)
    game = Game(tile_map)
    game.run()

if __name__ == "__main__":
    main()

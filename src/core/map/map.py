from src.core.map.tiles import TILE_REGISTRY, Tile
import random
import src.core.settings as settings


class TileMap:
    def __init__(self, tiles: list[list[int]], tile_size: int):
        self.tiles = tiles
        self.tile_size = tile_size

    @property
    def width(self):
        return len(self.tiles[0]) if self.tiles else 0
    
    @property
    def height(self):
        return len(self.tiles) if self.tiles else 0
        
    def set_tile(self, x: int, y: int, tile_type: int):
        if tile_type in TILE_REGISTRY:
            self.tiles[y][x] = tile_type
        else:
            raise ValueError(f"Tile type '{tile_type}' not found in registry.")

    def get_tile_at(self, x: int, y: int) -> Tile:
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return TILE_REGISTRY[self.tiles[y][x]]
        else:
            raise IndexError("Tile coordinates out of bounds.")
   

def generate_random_map(width: int, height: int, tile_probabilities: dict[int, float]) -> TileMap:
    """Generates a random map based on the provided tile probabilities."""
    tiles = [[random.choices(list(tile_probabilities.keys()), weights=tile_probabilities.values())[0] for _ in range(width)] for _ in range(height)]
    # replace boundary tiles with Solid tiles
    tiles[0] = [4 for _ in range(width)]
    tiles[height - 1] = [4 for _ in range(width)]
    for i in range(height):
        tiles[i][0] = 4
        tiles[i][-1] = 4
    return TileMap(tiles, tile_size=settings.TILE_SIZE)

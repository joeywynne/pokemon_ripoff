from src.core.map.grid_map import GridMap
from src.core.map.tiles import TILE_REGISTRY, Tile
from src.world_generation.biomes import BiomeType
from src.world_generation.region_map import RegionMap
from src.core import settings


class TileMap(GridMap):

    def __init__(self, width: int, height: int):
        # Initialize the grid with default tile type (e.g., "GRASS")
        default_tile_type = 1
        grid = [[default_tile_type for _ in range(width)] for _ in range(height)]
        super().__init__(grid, grid_size=settings.TILE_SIZE)

    def set_tile(self, x: int, y: int, tile_type: int):
        if tile_type in TILE_REGISTRY:
            self.grid[y][x] = tile_type
        else:
            raise ValueError(f"Tile type '{tile_type}' not found in registry.")

    def get_tile_at(self, x: int, y: int) -> Tile:
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
            return TILE_REGISTRY[self.grid[y][x]]
        else:
            raise IndexError("Tile coordinates out of bounds.")


def generate_tile_map(width: int, height: int, regions_map: RegionMap) -> TileMap:
    """
    Generates a tile map filled with the default tile type.
    """
    tile_map = TileMap(width, height)
    for y in range(height):
        for x in range(width):
            region = regions_map.grid[y][x]
            if region:
                # Assign tile type based on the region's biome
                if region.biome == BiomeType.FOREST:
                    tile_map.set_tile(x, y, 1)
                elif region.biome == BiomeType.GRASSLAND:
                    tile_map.set_tile(x, y, 1)
                elif region.biome == BiomeType.WATER:
                    tile_map.set_tile(x, y, 2)
                elif region.biome == BiomeType.URBAN:
                    tile_map.set_tile(x, y, 5)
            else:
                # Default tile type if no region is found
                tile_map.set_tile(x, y, 1)
    return tile_map

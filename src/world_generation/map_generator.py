from src.core.map.tile_map import TileMap
from src.world_generation.region import Region
from src.world_generation.region_map import TEST_REGIONS_SEED, RegionMap


class MapGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def generate_map(self) -> TileMap:
        """
        Generates a tile map with the given width and height.
        """
        regions = self.generate_regions(TEST_REGIONS_SEED)
        return regions

    def generate_regions(self, region_seeds: list[Region]) -> RegionMap:
        """
        Generates a 2D list of tile types based on the regions.
        """
        # Create a grid filled with None (no region)
        grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                # Find the closest region to this cell
                closest_region = min(
                    region_seeds,
                    key=lambda region: (region.centre_x - x) ** 2 + (region.centre_y - y) ** 2
                )
                grid[y][x] = closest_region

        return RegionMap(grid, grid_size=1)
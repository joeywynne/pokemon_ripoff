from src.core.map.grid_map import GridMap
from src.world_generation.region import Region
from src.world_generation.biomes import BiomeType

class RegionMap(GridMap):
    pass

TEST_REGIONS_SEED = [
    Region(biome=BiomeType.FOREST, name="Forest", centre_x=30, centre_y=15),
    Region(biome=BiomeType.GRASSLAND, name="Grassland", centre_x=8, centre_y=5),
    Region(biome=BiomeType.WATER, name="Lake", centre_x=38, centre_y=24),
    Region(biome=BiomeType.URBAN, name="City", centre_x=20, centre_y=45),
]

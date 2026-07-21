from src.core.map.grid_map import GridMap
from src.world_generation.region import Region
from src.world_generation.biomes import BiomeType

class RegionMap(GridMap):
    pass

TEST_REGIONS_SEED = [
    Region(biome=BiomeType.FOREST, name="Forest", centre_x=45, centre_y=20),
    Region(biome=BiomeType.GRASSLAND, name="Grassland", centre_x=15, centre_y=5),
    Region(biome=BiomeType.WATER, name="Lake", centre_x=60, centre_y=60),
    Region(biome=BiomeType.URBAN, name="City", centre_x=20, centre_y=45),
]

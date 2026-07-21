from dataclasses import dataclass
from src.world_generation.biomes import BiomeType


@dataclass
class Region:
    biome: BiomeType
    name: str
    centre_x: int
    centre_y: int


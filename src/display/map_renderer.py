import pygame
from src.core.map.map import TileMap
from src.core.settings import WHITE

class MapRenderer:
    def __init__(self, tile_map: TileMap):
        self.tile_map = tile_map

    def draw(self, surface: pygame.Surface):
        tile_size = self.tile_map.tile_size

        for ty in range(self.tile_map.height):
            for tx in range(self.tile_map.width):
                tile = self.tile_map.get_tile_at(tx, ty)
                rect = pygame.Rect(tx * tile_size, ty * tile_size, tile_size, tile_size)
                pygame.draw.rect(surface, tile.colour, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)

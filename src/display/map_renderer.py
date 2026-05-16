import pygame
from src.core.map.map import TileMap
from src.core.settings import WHITE
from src.core.camera import Camera
from src.display.assets import AssetStore

class MapRenderer:
    def __init__(self, tile_map: TileMap, assets: AssetStore):
        self.tile_map = tile_map
        self.assets = assets

    def draw(self, surface: pygame.Surface, camera: Camera):
        tile_size = self.tile_map.tile_size

        for ty in range(self.tile_map.height):
            for tx in range(self.tile_map.width):
                tile = self.tile_map.get_tile_at(tx, ty)
                
                world_x = tx * tile_size
                world_y = ty * tile_size
                screen_x = world_x - camera.x
                screen_y = world_y - camera.y

                dest = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
                if tile.texture:
                    texture = self.assets.image(tile.texture, alpha=True)
                    surface.blit(texture, dest)
                else:
                    pygame.draw.rect(surface, tile.colour, dest)
                # Grid lines for debugging
                pygame.draw.rect(surface, WHITE, dest, 1)

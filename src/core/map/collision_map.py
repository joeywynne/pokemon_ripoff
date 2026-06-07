from src.core.map.tile_map import TileMap
from src.core.map.grid_map import GridMap


class CollisionMap(GridMap):
    def is_cell_solid(self, idx_x: int, idx_y: int) -> bool:
        if 0 <= idx_y < self.height and 0 <= idx_x < self.width:
            return self.grid[idx_y][idx_x]
        else:
            # We are out of bounds.
            return True

    def collides(self, rect):
        for tx, ty in self.cells_overlapping_rect(rect):
            if self.is_cell_solid(tx, ty):
                tile_rect = self.grid_rect(tx, ty)
                if rect.colliderect(tile_rect):
                    return True
        return False


def generate_collision_map(tile_map: TileMap) -> CollisionMap:
    return CollisionMap(
        [
            [tile == 4 for tile in row]  # Only tile type 4 (Solid) is considered solid
            for row in tile_map.grid
        ],
        tile_map.grid_size,
    )

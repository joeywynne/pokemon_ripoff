import pygame

class GridMap:
    def __init__(self, grid: list[list], grid_size: int):
        self.grid_size = grid_size
        self.grid = grid

        self.width = len(self.grid[0]) if self.grid else 0
        self.height = len(self.grid) if self.grid else 0

    def grid_rect(self, tx: int, ty: int) -> pygame.Rect:
        gs = self.grid_size
        return pygame.Rect(tx * gs, ty * gs, gs, gs)
    
    def world_to_grid(self, x: int, y: int) -> tuple[int, int]:
        return (x // self.grid_size, y // self.grid_size)

    def cells_overlapping_rect(self, rect: pygame.Rect):
        x, y, w, h = rect
        left = int(x // self.grid_size)
        right = int((x + w - 1) // self.grid_size)
        top = int(y // self.grid_size)
        bottom = int((y + h - 1) // self.grid_size)

        for cy in range(top, bottom + 1):
            for cx in range(left, right + 1):
                yield (cx, cy)

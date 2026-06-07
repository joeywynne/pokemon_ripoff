import pygame
from pathlib import Path
from typing import Optional


class AssetStore:
    def __init__(self, tile_size: int, base_dir: str = "assets"):
        self.tile_size = tile_size
        self.base_dir = Path(base_dir)
        self._cache: dict[str, pygame.Surface] = {}

    def get_sprite(
        self,
        relative_path: str,
        position: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
        alpha: bool = True,
    ) -> pygame.Surface:
        """Load a sprite from the assets directory.

        If position and size provied then we obtain from the spritesheet.
        Otherwise we take the whole image.
        With optional alpha transparency.
        """
        key = f"{relative_path}_{alpha}_{self.tile_size}"
        if position:
            key = f"{key}_{position[0]}_{position[1]}"
        if key in self._cache:
            return self._cache[key]
        full_path = self.base_dir / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"Asset not found: {full_path}")

        image = pygame.image.load(full_path)
        if position and size:
            image = get_image_at(image, position, size)
        image = image.convert_alpha() if alpha else image.convert()

        if image.get_width() != self.tile_size or image.get_height() != self.tile_size:
            image = pygame.transform.scale(image, (self.tile_size, self.tile_size))

        self._cache[key] = image
        return image


def get_image_at(image, position, size, colourkey=None):
    """Loads image from x, y, x+offset, y+offset"""
    rect = pygame.Rect(position + size)
    image = pygame.Surface(rect.size).convert()
    image.blit(image, (0, 0), rect)
    if colourkey is not None:
        if colourkey == -1:
            colourkey = image.get_at((0, 0))
    image.set_colorkey(colourkey, pygame.RLEACCEL)
    return image

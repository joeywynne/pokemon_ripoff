import pygame
from pathlib import Path
from typing import Optional


class AssetStore:
    def __init__(self, base_dir: str = "assets"):
        self.base_dir = Path(base_dir)
        self._cache: dict[str, pygame.Surface] = {}

    def get_sprite(
        self,
        relative_path: str,
        entity_size: int,
        position: Optional[tuple[int, int]] = None,
        sheet_size: Optional[tuple[int, int]] = None,
        alpha: bool = True,
    ) -> pygame.Surface:
        """Load a sprite from the assets directory.

        If position and sheet_size are provided then we obtain from the spritesheet.
        Otherwise we take the whole image.
        With optional alpha transparency.
        """
        key = f"{relative_path}_{alpha}_{entity_size}"
        if position:
            key = f"{key}_{position[0]}_{position[1]}"
        if key in self._cache:
            return self._cache[key]
        full_path = self.base_dir / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"Asset not found: {full_path}")

        image = pygame.image.load(full_path)
        if position and sheet_size:
            image = get_image_from_spritesheet(image, position, sheet_size)
        image = image.convert_alpha() if alpha else image.convert()

        if image.get_width() != entity_size or image.get_height() != entity_size:
            image = pygame.transform.scale(image, (entity_size, entity_size))

        self._cache[key] = image
        return image


def get_image_from_spritesheet(image, position, sheet_size):
    """Extract a single tile from a spritesheet based on the given position and sheet size."""
    width = image.get_width()
    height = image.get_height()
    tile_width = width // sheet_size[0]
    tile_height = height // sheet_size[1]
    size = (tile_width, tile_height)
    return get_image_at(
        image, (position[0] * tile_width, position[1] * tile_height), size
    )


def get_image_at(
    image,
    position,
    size,
):
    """Loads image from x, y, x+offset, y+offset"""
    rect = pygame.Rect(position + size)
    new_image = pygame.Surface(rect.size).convert()
    new_image.blit(image, (0, 0), rect)
    return new_image

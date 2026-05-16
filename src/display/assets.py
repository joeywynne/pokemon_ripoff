import pygame
from pathlib import Path

class AssetStore:
    def __init__(self, tile_size: int, base_dir: str = "assets"):
        self.tile_size = tile_size
        self.base_dir = Path(base_dir)
        self._cache: dict[str, pygame.Surface] = {}

    def image(self, relative_path: str, alpha: bool = True) -> pygame.Surface:
        """Load an image from the assets directory, with optional alpha transparency."""
        key = f"{relative_path}_{alpha}_{self.tile_size}"
        if key in self._cache:
            return self._cache[key]

        full_path = self.base_dir / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"Asset not found: {full_path}")

        image = pygame.image.load(full_path)
        image = image.convert_alpha() if alpha else image.convert()

        if image.get_width() != self.tile_size or image.get_height() != self.tile_size:
            image = pygame.transform.scale(image, (self.tile_size, self.tile_size))

        self._cache[relative_path] = image
        return image
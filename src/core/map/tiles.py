from src.core.settings import WHITE, BLACK, RED, BLUE, GREEN, BROWN
from typing import Tuple, Optional

Colour = Tuple[int, int, int]


class Tile:
    "Defines the base tile on the map. No effects or interactions."

    is_passable: bool = True
    speed_modifier: float = 1.0
    colour: Colour = WHITE
    texture: Optional[str] = None

    @property
    def has_action(self):
        return hasattr(self, "action") and callable(getattr(self, "action"))


class GrassTile(Tile):
    "Grass textured tile with speed modifier."

    speed_modifier: float = 0.8
    colour: Colour = GREEN
    texture: Optional[str] = "tiles/highland.png"


class WaterTile(Tile):
    "Water textured tile with speed modifier."

    speed_modifier: float = 1.2
    colour: Colour = BLUE
    texture: Optional[str] = "tiles/water.png"


class GroundTile(Tile):
    "Ground textured tile with speed modifier."

    colour: Colour = BROWN
    texture: Optional[str] = "tiles/path.png"


class ActionTile(Tile):
    "Adds red colour and triggers an event when stepped on."

    colour: Colour = RED

    def action(self):
        print("Action triggered! This could be a battle, item pickup, etc.")


class SolidTile(Tile):
    "Solid Tile which is not passable"

    is_passable: bool = False
    colour: Colour = BLACK


TILE_REGISTRY = {
    0: Tile(),
    1: GrassTile(),
    2: WaterTile(),
    3: ActionTile(),
    4: SolidTile(),
    5: GroundTile(),
}

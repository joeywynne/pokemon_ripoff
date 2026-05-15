from src.core.settings import WHITE, BLACK, RED, BLUE, GREEN

class Tile:
    "Defines the base tile on the map. No effects or interactions."
    is_passable: bool = True
    speed_modifier: float = 1.0
    colour: tuple = WHITE

    @property
    def has_action(self):
        return hasattr(self, 'action') and callable(getattr(self, 'action'))

class GrassTile(Tile):
    "Adds green colour and slows movement speed by 20%."
    speed_modifier: float = 0.8
    colour: tuple = GREEN

class WaterTile(Tile):
    "Adds blue colour and increases movement speed by 20%."
    speed_modifier: float = 1.2
    colour: tuple = BLUE

class ActionTile(Tile):
    "Adds red colour and triggers an event when stepped on."
    colour: tuple = RED

    def action(self):
        print("Action triggered! This could be a battle, item pickup, etc.")

class SolidTile(Tile):
    "Solid Tile which is not passable"
    is_passable: bool = False
    colour: tuple = BLACK

TILE_REGISTRY = {
    0: Tile(),
    1: GrassTile(),
    2: WaterTile(),
    3: ActionTile(),
    4: SolidTile()
}

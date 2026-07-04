import logging
import pygame
from src.core.map.collision_map import CollisionMap
from src.core.map.tile_map import TileMap
from src.core.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from src.display.map_renderer import MapRenderer
from src.entities.player import Player
from src.entities.pokemon import generate_pokemon
from src.display.renderer import Renderer
from src.display.entities_renderer import EntitiesRenderer
from src.core.camera import Camera
from src.display.assets import AssetStore
from src.behaviours.movement_system import move_entities
from src.contracts import UpdateContext
from src.core.game_state import GameState
from src.ui.renderers.party_renderer import PartyRenderer
from src.ui.screens.party_screen import PartyScreen
from src.ui.ui_handler import UIManager

logger = logging.getLogger(__name__)


class Game:
    def __init__(
        self, tile_map: TileMap, collision_map: CollisionMap, debug: bool = False
    ):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokemon Ripoff")
        self.clock = pygame.time.Clock()
        self.running = True
        self.debug = debug
        self.collision_map = collision_map
        self.font = pygame.font.SysFont("consolas", 24) if self.debug else None

        assets = AssetStore()
        map_renderer = MapRenderer(tile_map, assets)

        self.map_width = tile_map.width * tile_map.grid_size
        self.map_height = tile_map.height * tile_map.grid_size
        self.camera = Camera(
            SCREEN_WIDTH, SCREEN_HEIGHT, self.map_width, self.map_height
        )
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pokemon = generate_pokemon(6, self.map_width, self.map_height)

        self.entities = self.pokemon + [self.player]
        entities_renderer = EntitiesRenderer(self.entities, assets)
        self.renderer = Renderer(self.screen, entities_renderer, map_renderer)
        self.last_log_time = pygame.time.get_ticks()

        self.game_state = GameState.new_game()
        self.ui_handler = UIManager()

        logger.debug("Game initialized with debug=%s", self.debug)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.ui_handler.has_screen:
                self.ui_handler.handle_event(event)
            else:
                self.handle_game_event(event)

    def handle_game_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.open_party_screen()
            elif event.key == pygame.K_i:
                self.open_inventory_screen()

    def open_inventory_screen(self):
        logger.info("Opening inventory screen")
        pass

    def close_inventory_screen(self, inventory_screen):
        logger.info("Closing inventory screen")
        self.ui_handler.close()

    def open_party_screen(self):
        screen = PartyScreen(
            game_state=self.game_state,
            on_close=self.close_party_screen,
            renderer=PartyRenderer(),
        )
        self.ui_handler.open(screen)

    def close_party_screen(self, party_screen):
        self.commit_party_changes(party_screen.buddy_index)
        self.ui_handler.close()

    def commit_party_changes(self, buddy_index):
        buddy = self.game_state.swap_buddy(
            buddy_index,
            self.player.x + self.player.size / 2,
            self.player.y + self.player.size / 2,
        )

        self.entities[:] = [entity for entity in self.entities if entity.is_active]

        if buddy:
            self.entities.append(buddy)

    def update(self):
        keys = pygame.key.get_pressed()

        if self.ui_handler.has_screen:
            self.ui_handler.update(keys)
        else:
            self.update_game(keys)

        self.log_debug_info()

    def update_game(self, keys):
        # Get the desired moves for all entities
        new_entities = []
        for entity in self.entities:
            context = UpdateContext(
                keys=keys,
                nearby_pokemon=self.pokemon,
                player_position=(self.player.x, self.player.y),
                map_size=(self.map_width, self.map_height),
            )
            pokeball = entity.update_intended(context)
            if pokeball:
                new_entities.append(pokeball)

        # Add the pokeball to the entities list if it was created
        if new_entities != []:
            self.entities.extend(new_entities)

        move_entities(self.entities, self.collision_map, self.game_state)

    def render(self):
        fps_text = None
        if self.debug and self.font:
            fps = self.clock.get_fps()
            fps_text = self.font.render(f"FPS: {fps:.1f}", True, (255, 255, 0))

        self.renderer.render(self.player, self.camera, fps_text, self.debug)
        self.ui_handler.render(self.screen)

        pygame.display.flip()

    def log_debug_info(self):
        if not self.debug:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_log_time >= 1000:  # Log every second
            logger.debug("Player position: (%.2f, %.2f)", self.player.x, self.player.y)
            logger.debug("Player velocity: (%.2f, %.2f)", *self.player.velocity)
            logger.debug(
                "Player desired velocity: (%.2f, %.2f)", *self.player.desired_velocity
            )
            logger.debug(len(self.entities))
            self.last_log_time = current_time

    def run(self):
        logger.info("Starting game loop")
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        logger.info("Game shut down")

import logging
import pygame
from src.movement.collision_resolution import resolve_all_collisions
from src.core.map.collision_map import CollisionMap
from src.core.map.tile_map import TileMap
from src.core.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from src.display.map_renderer import MapRenderer
from src.entities.player import Player
from src.entities.npc import generate_npcs
from src.display.renderer import Renderer
from src.display.entities_renderer import EntitiesRenderer
from src.core.settings import PURPLE
from src.core.camera import Camera
from src.display.assets import AssetStore
from src.movement.system import MovementSystem


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

        map_width = tile_map.width * tile_map.grid_size
        map_height = tile_map.height * tile_map.grid_size
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_width, map_height)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PURPLE)
        self.npcs = generate_npcs(4, map_width, map_height)

        self.entities = self.npcs + [self.player]
        entities_renderer = EntitiesRenderer(self.entities, assets)
        self.renderer = Renderer(self.screen, entities_renderer, map_renderer)
        self.last_log_time = pygame.time.get_ticks()

        logger.debug("Game initialized with debug=%s", self.debug)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        pokeball = self.player.update(keys=keys)
        if pokeball is not None:
            self.entities.append(pokeball)

        for entity in self.entities:
            if entity is not self.player:
                entity.update()
                MovementSystem.move_entity(entity, self.collision_map)
                if not entity.is_active:
                    self.entities.remove(entity)
        resolve_all_collisions(self.entities, self.collision_map)
        
        for entity in self.entities:
            MovementSystem.final_safety(entity, self.collision_map)

        if self.debug:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_log_time > 1000:  # Log every second
                logger.debug("Player position: (%s, %s)", self.player.x, self.player.y)
                logger.debug("Player velocity: %s", self.player.velocity)
                logger.debug("Player facing: %s", self.player.facing)
                self.last_log_time = current_time

    def render(self):
        fps_text = None
        if self.debug and self.font:
            fps = self.clock.get_fps()
            fps_text = self.font.render(f"FPS: {fps:.1f}", True, (255, 255, 0))

        self.renderer.render(self.player, self.camera, fps_text, self.debug)

    def run(self):
        logger.info("Starting game loop")
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        logger.info("Game shut down")

import pygame
from src.core.map.map import TileMap
from src.core.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from src.display.map_renderer import MapRenderer
from src.entities.player import Player
from src.display.renderer import Renderer
from src.display.entities_renderer import EntitiesRenderer
from src.core.settings import PURPLE

class Game:
    def __init__(self, tile_map: TileMap):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokemon Ripoff")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PURPLE)
        map_renderer = MapRenderer(tile_map)
        entities = [self.player]
        entities_renderer = EntitiesRenderer(entities)
        self.renderer = Renderer(self.screen, map_renderer, entities_renderer)
        self.last_log_time = pygame.time.get_ticks()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Log player position
        current_time = pygame.time.get_ticks()
        if current_time - self.last_log_time > 1000:  # Log every second
            print(f"Player position: ({self.player.x}, {self.player.y})")
            self.last_log_time = current_time

    def render(self):
        self.renderer.render()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()

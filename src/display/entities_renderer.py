from typing import Optional
import pygame
from src.display.assets import AssetStore
from src.entities.entity import Entity
from src.entities.pokeball import Projectile
from src.core.camera import Camera
from src.entities.pokemon import Pokemon


class EntitiesRenderer:
    def __init__(self, entities: list[Entity], assets: AssetStore):
        self.entities = entities
        self.assets = assets

    def draw_entity(
        self,
        surface: pygame.Surface,
        entity: Entity,
        camera: Camera,
        target_entity,
        debug: Optional[bool] = False,
    ):
        scale_y = 1
        scale_x = 1
        if isinstance(entity, Projectile):
            behaviour = entity.movement_controller
            if behaviour.vz < 0:
                scale_y = 0.95
                scale_x = 1.05
            elif entity.squash_timer > 0:
                scale_y = 0.75
                scale_x = 1.15
            shadow_pos = (
                int(entity.x - camera.x + entity.size * 0.5),
                int(entity.y - camera.y + entity.size),
            )
            pygame.draw.circle(
                surface, (50, 50, 50), shadow_pos, entity.size // 3
            )  # Draw shadow as a circle

        rect = entity.get_rect()
        screen_rect = rect.move(-int(camera.x), -int(camera.y))
        if getattr(entity, "sprite_info", None):
            sprite = self.assets.get_sprite(
                entity.sprite_info.relative_path,
                entity.size,
                position=entity.sprite_info.position,
                sprite_size=entity.sprite_info.sprite_size,
            )

            sprite = pygame.transform.rotate(sprite, entity.rotation)
            sprite = pygame.transform.scale(
                sprite, (int(entity.size * scale_x), int(entity.size * scale_y))
            )

            if isinstance(entity, Pokemon):
                self.draw_health_bar(surface, entity, screen_rect)
                self.draw_catch_probability_bar(surface, entity, screen_rect)
                if entity == target_entity:
                    self.draw_target_indicator(surface, entity, screen_rect)
            sprite_rect = sprite.get_rect()
            sprite_rect.center = (
                screen_rect.centerx,
                screen_rect.centery - int(entity.z * 1.0),
            )

            surface.blit(sprite, sprite_rect)
        else:
            pygame.draw.rect(surface, entity.colour, screen_rect)

        if debug:
            pygame.draw.rect(
                surface, (255, 0, 0), screen_rect, 1
            )  # Red outline for debugging

    def draw_health_bar(
        self, surface: pygame.Surface, pokemon: Pokemon, screen_rect: pygame.Rect
    ):
        bar_width = screen_rect.width
        bar_height = 5
        bar_x = screen_rect.x
        bar_y = screen_rect.y - bar_height - 2  # Position above the Pokemon

        # Calculate health percentage
        health_percentage = max(pokemon.hp / pokemon.species.base_hp, 0)

        # Determine health bar color based on health percentage
        if health_percentage > 0.5:
            bar_color = (0, 255, 0)  # Green
        elif health_percentage > 0.2:
            bar_color = (255, 255, 0)  # Yellow
        else:
            bar_color = (255, 0, 0)  # Red

        # Draw the background of the health bar (gray)
        pygame.draw.rect(
            surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height)
        )

        # Draw the current health portion of the health bar
        current_health_width = int(bar_width * health_percentage)
        pygame.draw.rect(
            surface, bar_color, (bar_x, bar_y, current_health_width, bar_height)
        )

    def draw_catch_probability_bar(
        self, surface: pygame.Surface, pokemon: Pokemon, screen_rect: pygame.Rect
    ):
        bar_width = screen_rect.width
        bar_height = 5
        bar_x = screen_rect.x
        bar_y = screen_rect.y - bar_height - 10  # Position above the health bar

        # Calculate catch probability
        catch_probability = max(pokemon.get_approx_catch_probability(), 0)

        # Determine catch probability bar color based on probability
        if catch_probability > 0.5:
            bar_color = (0, 255, 0)  # Green
        elif catch_probability > 0.2:
            bar_color = (255, 255, 0)  # Yellow
        else:
            bar_color = (255, 0, 0)  # Red

        # Draw the background of the health bar (gray)
        pygame.draw.rect(
            surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height)
        )

        # Draw the current health portion of the health bar
        current_health_width = int(bar_width * catch_probability)
        pygame.draw.rect(
            surface, bar_color, (bar_x, bar_y, current_health_width, bar_height)
        )

    def draw_target_indicator(self, surface, target_pokemon: Pokemon, screen_rect):
        indicator_size = max(target_pokemon.size / 2, 20)
        indicator_x = screen_rect.x + (target_pokemon.size / 2)
        indicator_y = screen_rect.y - 22 # Above health bar

        sprite = self.assets.get_sprite("target.png", indicator_size)
        sprite_rect = sprite.get_rect()
        sprite_rect.center = (indicator_x, indicator_y)

        surface.blit(sprite, sprite_rect)
        

    def draw(
        self, surface: pygame.Surface, camera: Camera, target_entity, debug: Optional[bool] = False
    ):
        for entity in self.entities:
            self.draw_entity(surface, entity, camera, target_entity, debug)

import pygame

from src.core import settings
import random


class MovementBehaviour:

    def get_intended_move(self, entity, **kwargs) -> tuple[float, float]:
        # Default to no movement
        return 0, 0


class PlayerBehaviour(MovementBehaviour):
    def get_intended_move(self, entity, keys: dict) -> tuple[float, float]:
        # Default to no movement if no movement keys are pressed
        dy = 0
        dx = 0

        if keys[pygame.K_LEFT]:
            dx -= entity.speed
        if keys[pygame.K_RIGHT]:
            dx += entity.speed
        if keys[pygame.K_UP]:
            dy -= entity.speed
        if keys[pygame.K_DOWN]:
            dy += entity.speed

        return dx, dy


class PokeballBehaviour(MovementBehaviour):
    def __init__(self, facing: tuple = (1, 0), throw_power: float = 5.0):
        self.facing = facing
        self.throw_power = throw_power

        # Compute an initial velocity from facing direction and throw power.
        clamped_power = max(1.0, min(self.throw_power, 60.0))
        base_speed = 5.0
        magnitude = min(40.0, 1.0 + clamped_power / 10.0) * base_speed
        self.velocity = (self.facing[0] * magnitude, self.facing[1] * magnitude)
        self.vz = magnitude * 0.75

        # Damping factor for vertical velocity after bounce
        self.bounce_damping = 0.5
        # Minimum vertical velocity to continue bouncing
        self.min_bounce_velocity = 0.25
        # Damping factor for horizontal velocity to simulate air resistance
        self.air_resistance = 0.97
        self.ground_resistance = 0.94
        # Minimum horizontal velocity to be considered active
        self.min_horizontal_velocity = 0.05

    def get_intended_move(self, entity, **kwargs) -> tuple[float, float]:
        if entity.squash_timer > 0:
            entity.squash_timer -= 1

        self._update_vertical_arc(entity)
        self._update_horizontal_velocity(entity)
        self._set_active_timer(entity)

        if entity.start_deactivating:
            entity.active_timer -= 1
        if entity.active_timer <= 0:
            entity.is_active = False

        entity.rotation -= self.velocity[0] * 2.0

        return self.velocity

    def _update_vertical_arc(self, entity):
        self.vz -= settings.GRAVITY
        entity.z += self.vz

        if entity.z < 0:
            entity.z = 0
            self.vz = -self.vz * self.bounce_damping
            entity.squash_timer = 6.0

            if abs(self.vz) < self.min_bounce_velocity:
                self.vz = 0

    def _update_horizontal_velocity(self, entity):
        # If on floor should be more resistant to horizontal movement
        if entity.z < 0.1:
            resistance_factor = self.air_resistance * self.ground_resistance
        else:
            resistance_factor = self.air_resistance

        self.velocity = (
            self.velocity[0] * resistance_factor,
            self.velocity[1] * resistance_factor,
        )

    def _set_active_timer(self, entity):
        horizontal_speed = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        if (
            entity.z == 0
            and self.vz == 0
            and horizontal_speed < self.min_horizontal_velocity
        ):
            entity.start_deactivating = True


class StationaryBehaviour(MovementBehaviour):
    def get_intended_move(self, entity, **kwargs) -> tuple[float, float]:
        return 0, 0


class PacingBehaviour(MovementBehaviour):
    def __init__(self, axis: str, distance: float = 180.0):
        """
        axis: 'horizontal' or 'vertical'
        distance: the distance to pace before changing direction
        """
        self.axis = axis
        self.distance = distance
        self.direction = 1
        self.travelled = 0

    def get_intended_move(self, entity, **kwargs) -> tuple[float, float]:
        if self.axis == "horizontal":
            dx = entity.speed * self.direction
            dy = 0
            movement_amount = abs(dx)
        else:
            dx = 0
            dy = entity.speed * self.direction
            movement_amount = abs(dy)

        self.travelled += movement_amount
        if self.travelled >= self.distance:
            self.direction *= -1
            self.travelled = 0

        return dx, dy


class WanderBehaviour(MovementBehaviour):
    def __init__(
        self,
        min_interval: int = 60,
        max_interval: int = 120,
        allow_stationary: bool = True,
    ):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.allow_stationary = allow_stationary

        self.timer = 0
        self.direction = (0, 0)
        self.change_interval = random.randint(self.min_interval, self.max_interval)

    def get_intended_move(self, entity, **kwargs) -> tuple[float, float]:
        self.timer += 1
        if self.timer >= self.change_interval:
            self.timer = 0
            self.change_interval = random.randint(self.min_interval, self.max_interval)
            self.direction = self._random_direction()

        dx = entity.speed * self.direction[0]
        dy = entity.speed * self.direction[1]
        return dx, dy

    def _random_direction(self) -> tuple[int, int]:
        options = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        if self.allow_stationary:
            options.append((0, 0))

        return random.choice(options)


class FollowBehaviour(MovementBehaviour):

    def get_intended_move(
        self, entity, player_position, speed_multiplier
    ) -> tuple[float, float]:
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx**2 + dy**2) ** 0.5
        # Normalize the direction vector and scale by speed
        if distance != 0:
            dx = (dx / distance) * entity.speed * speed_multiplier
            dy = (dy / distance) * entity.speed * speed_multiplier
        else:
            dx = 0
            dy = 0

        return dx, dy


class FleeBehaviour(MovementBehaviour):

    def get_intended_move(
        self, entity, player_position, speed_multiplier
    ) -> tuple[float, float]:
        dx = entity.x - player_position[0]
        dy = entity.y - player_position[1]
        distance = (dx**2 + dy**2) ** 0.5
        # Normalize the direction vector and scale by speed
        if distance != 0:
            dx = (dx / distance) * entity.speed * speed_multiplier
            dy = (dy / distance) * entity.speed * speed_multiplier
        else:
            dx = 0
            dy = 0

        return dx, dy

class TeleportBehaviour(MovementBehaviour):
    def get_intended_move(self, entity, map_size, teleport_frac=1.0, **kwargs) -> tuple[float, float]:
        if teleport_frac <= 0.0:
            # Calculate a random teleport destination within the map boundaries
            target_x = random.randint(settings.TILE_SIZE, map_size[0] - settings.TILE_SIZE)
            target_y = random.randint(settings.TILE_SIZE, map_size[1] - settings.TILE_SIZE)

            dx = target_x - entity.x
            dy = target_y - entity.y
            return dx, dy
        else:
            entity.size = entity.species.size * teleport_frac
            return 0, 0

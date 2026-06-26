import pygame

from src.core import settings
import random


class MovementBehaviour:

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
        # Default to no movement
        return 0, 0


class PlayerBehaviour(MovementBehaviour):
    def get_intended_move(self, player, update_context) -> tuple[float, float]:
        keys = update_context.keys
        # Default to no movement if no movement keys are pressed
        dy = 0
        dx = 0

        if keys[pygame.K_LEFT]:
            dx -= player.speed
        if keys[pygame.K_RIGHT]:
            dx += player.speed
        if keys[pygame.K_UP]:
            dy -= player.speed
        if keys[pygame.K_DOWN]:
            dy += player.speed

        return dx, dy


class PokeballBehaviour(MovementBehaviour):
    def __init__(self, facing: tuple = (1, 0), throw_power: float = 5.0):
        self.facing = facing
        self.throw_power = throw_power

        # Compute an initial velocity from facing direction and throw power.
        clamped_power = max(1.0, min(self.throw_power, settings.MAX_THROW_POWER))
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

    def get_intended_move(self, pokeball, update_context) -> tuple[float, float]:
        if pokeball.squash_timer > 0:
            pokeball.squash_timer -= 1

        self._update_vertical_arc(pokeball)
        self._update_horizontal_velocity(pokeball)
        self._set_active_timer(pokeball)

        if pokeball.start_deactivating:
            pokeball.active_timer -= 1
        if pokeball.active_timer <= 0:
            pokeball.is_active = False

        pokeball.rotation -= self.velocity[0] * 2.0

        return self.velocity

    def _update_vertical_arc(self, pokeball):
        self.vz -= settings.GRAVITY
        pokeball.z += self.vz

        if pokeball.z < 0:
            pokeball.z = 0
            self.vz = -self.vz * self.bounce_damping
            pokeball.squash_timer = 6.0

            if abs(self.vz) < self.min_bounce_velocity:
                self.vz = 0

    def _update_horizontal_velocity(self, pokeball):
        # If on floor should be more resistant to horizontal movement
        if pokeball.z < 0.1:
            resistance_factor = self.air_resistance * self.ground_resistance
        else:
            resistance_factor = self.air_resistance

        self.velocity = (
            self.velocity[0] * resistance_factor,
            self.velocity[1] * resistance_factor,
        )

    def _set_active_timer(self, pokeball):
        horizontal_speed = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        if (
            pokeball.z == 0
            and self.vz == 0
            and horizontal_speed < self.min_horizontal_velocity
        ):
            pokeball.start_deactivating = True


class StationaryBehaviour(MovementBehaviour):
    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
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

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
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

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
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

    def __init__(
        self,
        previous_behaviour: MovementBehaviour,
        speed_multiplier: float = 1.0,
        duration: int = 300,
    ):
        self.previous_behaviour = previous_behaviour
        self.speed_multiplier = speed_multiplier
        self.duration = duration

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
        self.duration -= 1

        if self.duration <= 0:
            entity.movement_controller = self.previous_behaviour
            return 0, 0

        player_position = update_context.player_position
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx**2 + dy**2) ** 0.5
        # Normalize the direction vector and scale by speed
        if distance != 0:
            dx = (dx / distance) * entity.speed * self.speed_multiplier
            dy = (dy / distance) * entity.speed * self.speed_multiplier
        else:
            dx = 0
            dy = 0

        return dx, dy


class FleeBehaviour(MovementBehaviour):

    def __init__(
        self, previous_behaviour, speed_multiplier: float = 1.0, duration: int = 300
    ):
        self.speed_multiplier = speed_multiplier
        self.previous_behaviour = previous_behaviour
        self.duration = duration

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
        self.duration -= 1

        if self.duration <= 0:
            entity.movement_controller = self.previous_behaviour
            return 0, 0

        player_position = update_context.player_position
        dx = entity.x - player_position[0]
        dy = entity.y - player_position[1]
        distance = (dx**2 + dy**2) ** 0.5
        # Normalize the direction vector and scale by speed
        if distance != 0:
            dx = (dx / distance) * entity.speed * self.speed_multiplier
            dy = (dy / distance) * entity.speed * self.speed_multiplier
        else:
            dx = 0
            dy = 0

        return dx, dy


class TeleportBehaviour(MovementBehaviour):
    def __init__(self, teleport_frac: float = 1.0):
        self.teleport_frac = teleport_frac

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
        map_size = update_context.map_size
        if self.teleport_frac <= 0.0:
            # Calculate a random teleport destination within the map boundaries
            target_x = random.randint(
                settings.TILE_SIZE, map_size[0] - settings.TILE_SIZE
            )
            target_y = random.randint(
                settings.TILE_SIZE, map_size[1] - settings.TILE_SIZE
            )

            dx = target_x - entity.x
            dy = target_y - entity.y
            return dx, dy
        else:
            entity.size = entity.species.size * self.teleport_frac
            return 0, 0

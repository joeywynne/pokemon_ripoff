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

        self.bounce_damping = 0.5  # Damping factor for vertical velocity after bounce
        self.min_bounce_velocity = (
            0.25  # Minimum vertical velocity to continue bouncing
        )
        self.air_resistance = (
            0.98  # Damping factor for horizontal velocity to simulate air resistance
        )

    def get_intended_move(self, entity) -> tuple[float, float]:
        # Return the intended move based on current velocity
        self.vz -= settings.GRAVITY  # Simulate gravity effect on vertical velocity
        entity.z += self.vz  # Update vertical position
        if entity.z < 0:
            entity.z = 0
            self.vz = -self.vz * self.bounce_damping  # Bounce effect with energy loss

            if (
                self.vz < self.min_bounce_velocity
            ):  # If the vertical velocity is very small, stop bouncing
                self.vz = 0

        # dampen velocity
        self.velocity = (
            self.velocity[0] * self.air_resistance,
            self.velocity[1] * self.air_resistance,
        )
        return self.velocity


class StationaryBehaviour(MovementBehaviour):
    def get_intended_move(self, entity) -> tuple[float, float]:
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

    def get_intended_move(self, entity) -> tuple[float, float]:
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

    def get_intended_move(self, entity) -> tuple[float, float]:
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

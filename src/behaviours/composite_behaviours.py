from enum import Enum, auto
from typing import Callable

from src.behaviours.behaviour import (
    MovementBehaviour,
    WanderBehaviour,
    StationaryBehaviour,
    FleeBehaviour,
    FollowBehaviour,
    TeleportBehaviour,
)
import random


class BehaviourState(Enum):
    WANDER = auto()
    IDLE = auto()   
    FOLLOW = auto()
    FLEE = auto()
    TELEPORT = auto()


class StationaryWanderBehaviour(MovementBehaviour):

    def __init__(self):
        self.wander = WanderBehaviour()
        self.idle = StationaryBehaviour()

        self.state = BehaviourState.WANDER
        self.timer = random.randint(120, 300)

    def get_intended_move(self, entity, update_context):

        self.timer -= 1

        if self.timer <= 0:

            self.state = BehaviourState.IDLE if self.state == BehaviourState.WANDER else BehaviourState.WANDER

            self.timer = random.randint(120, 300)

        if self.state == BehaviourState.WANDER:
            return self.wander.get_intended_move(entity, update_context)

        return self.idle.get_intended_move(entity, update_context)


class PredicateSelectorBehaviour(MovementBehaviour):
    """Selects between two child behaviours using a stateful predicate."""

    def __init__(
        self,
        primary_behaviour: MovementBehaviour,
        secondary_behaviour: MovementBehaviour,
        should_use_secondary: Callable[[bool, object, object], bool],
        use_secondary_initially: bool = False,
    ):
        self.primary_behaviour = primary_behaviour
        self.secondary_behaviour = secondary_behaviour
        self.should_use_secondary = should_use_secondary
        self.use_secondary = use_secondary_initially

    def get_intended_move(self, entity, update_context):
        self.use_secondary = self.should_use_secondary(
            self.use_secondary,
            entity,
            update_context,
        )

        if self.use_secondary:
            return self.secondary_behaviour.get_intended_move(entity, update_context)

        return self.primary_behaviour.get_intended_move(entity, update_context)


class DistanceSelectorBehaviour(PredicateSelectorBehaviour):
    """Switches to secondary when near, back to primary when far enough."""

    def __init__(
        self,
        primary_behaviour: MovementBehaviour,
        secondary_behaviour: MovementBehaviour,
        start_secondary_distance: float,
        stop_secondary_distance: float,
    ):
        self.start_secondary_distance = start_secondary_distance
        self.stop_secondary_distance = stop_secondary_distance
        super().__init__(
            primary_behaviour=primary_behaviour,
            secondary_behaviour=secondary_behaviour,
            should_use_secondary=self._should_use_secondary,
        )

    def _should_use_secondary(self, currently_secondary: bool, entity, update_context) -> bool:
        player_position = update_context.player_position
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx**2 + dy**2) ** 0.5

        # Hysteresis prevents rapid state flapping near the threshold.
        if distance < self.start_secondary_distance:
            return True

        if distance > self.stop_secondary_distance:
            return False

        return currently_secondary


class WanderFollowBehaviour(MovementBehaviour):

    def __init__(
        self, start_follow_distance=100, stop_follow_distance=150, speed_multiplier=3.0
    ):
        self.selector = DistanceSelectorBehaviour(
            primary_behaviour=WanderBehaviour(),
            secondary_behaviour=FollowBehaviour(speed_multiplier=speed_multiplier),
            start_secondary_distance=start_follow_distance,
            stop_secondary_distance=stop_follow_distance,
        )

    def get_intended_move(self, entity, update_context):
        return self.selector.get_intended_move(entity, update_context)


class WanderFleeBehaviour(MovementBehaviour):

    def __init__(
        self, start_flee_distance=100, stop_flee_distance=150, speed_multiplier=3.0
    ):
        self.selector = DistanceSelectorBehaviour(
            primary_behaviour=WanderBehaviour(),
            secondary_behaviour=FleeBehaviour(speed_multiplier=speed_multiplier),
            start_secondary_distance=start_flee_distance,
            stop_secondary_distance=stop_flee_distance,
        )

    def get_intended_move(self, entity, update_context):
        return self.selector.get_intended_move(entity, update_context)


class StationaryTeleportBehaviour(MovementBehaviour):

    def __init__(self, teleport_distance=150):
        self.state = BehaviourState.IDLE
        self.idle = StationaryBehaviour()
        self.teleport = TeleportBehaviour()
        self.teleport_distance = teleport_distance

    def get_intended_move(self, entity, update_context):
        player_position = update_context.player_position
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.teleport_distance or self.state == BehaviourState.TELEPORT:
            self.state = BehaviourState.TELEPORT
        else:
            self.state = BehaviourState.IDLE

        if self.state == BehaviourState.TELEPORT:
            dx, dy = self.teleport.get_intended_move(entity, update_context)

        else:
            dx, dy = self.idle.get_intended_move(entity, update_context)

        if abs(dy) + abs(dx) > 0:
            self.state = BehaviourState.IDLE

        return dx, dy

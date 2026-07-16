from enum import Enum, auto

from src.behaviours.behaviour import (
    MovementBehaviour,
    WanderBehaviour,
    StationaryBehaviour,
    FleeBehaviour,
    FollowBehaviour,
    TeleportBehaviour,
)
import random

from src.behaviours.targeting_system import NearestTargeting


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
            self.state = (
                BehaviourState.IDLE
                if self.state == BehaviourState.WANDER
                else BehaviourState.WANDER
            )
            self.timer = random.randint(120, 300)

        if self.state == BehaviourState.WANDER:
            return self.wander.get_intended_move(entity, update_context)

        return self.idle.get_intended_move(entity, update_context)


class WanderFollowBehaviour(MovementBehaviour):

    def __init__(self, speed_multiplier=1.0, min_distance=50):
        self.speed_multiplier = speed_multiplier
        self.wander = WanderBehaviour(allow_stationary=False)
        self.follow = FollowBehaviour(
            speed_multiplier=speed_multiplier, min_distance=min_distance
        )
        self.follow_targeting = NearestTargeting(
            start_targeting_distance=100, stop_targeting_distance=150
        )

    def get_intended_move(self, entity, update_context):
        target = self.follow_targeting.get_target(
            entity, update_context.nearby_entities
        )
        if target is not None:
            return self.follow.get_intended_move(entity, target)
        return self.wander.get_intended_move(entity, update_context)


class WanderFleeBehaviour(MovementBehaviour):

    def __init__(self, speed_multiplier=1.0):
        self.speed_multiplier = speed_multiplier
        self.flee = FleeBehaviour(speed_multiplier=speed_multiplier)
        self.wander = WanderBehaviour()
        self.flee_targeting = NearestTargeting(
            start_targeting_distance=100, stop_targeting_distance=150
        )

    def get_intended_move(self, entity, update_context):
        target = self.flee_targeting.get_target(entity, update_context.nearby_entities)
        if target is not None:
            return self.flee.get_intended_move(entity, target)
        return self.wander.get_intended_move(entity, update_context)


class StationaryTeleportBehaviour(MovementBehaviour):

    def __init__(self, teleport_distance=150):
        self.state = BehaviourState.IDLE
        self.idle = StationaryBehaviour()
        self.teleport = TeleportBehaviour()
        self.teleport_distance = teleport_distance

    def get_intended_move(self, entity, update_context):
        dx = update_context.player_position.x - entity.x
        dy = update_context.player_position.y - entity.y
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


class BuddyBehaviour(MovementBehaviour):
    def __init__(
        self,
        wander_speed_mult: float = 0.5,
        wander_min_distance: int = 30,
        follow_speed_mult: float = 2.0,
        follow_min_distance: int = 10,
    ):
        self.follow_player = WanderFollowBehaviour(
            speed_multiplier=wander_speed_mult, min_distance=wander_min_distance
        )
        self.attack = FollowBehaviour(
            speed_multiplier=follow_speed_mult, min_distance=follow_min_distance
        )
        self.attack_target = None

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
        if self.attack_target:
            # Target is Pokemon - chase it
            return self.attack.get_intended_move(entity, self.attack_target)
        else:
            # No target - follow player
            return self.follow_player.get_intended_move(entity, update_context.player_position)

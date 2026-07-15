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
        self.wander = WanderBehaviour()
        self.follow = FollowBehaviour(
            speed_multiplier=speed_multiplier, min_distance=min_distance
        )

    def get_intended_move(self, entity, update_context):
        if entity.target is not None:
            return self.follow.get_intended_move(entity, update_context)
        return self.wander.get_intended_move(entity, update_context)


class WanderFleeBehaviour(MovementBehaviour):

    def get_intended_move(self, entity, update_context):
        if entity.target is not None:
            return FleeBehaviour(speed_multiplier=1.0).get_intended_move(
                entity, update_context
            )
        return WanderBehaviour().get_intended_move(entity, update_context)


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


class BuddyBehaviour(MovementBehaviour):
    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
        if entity.target is not None:
            # Target is Pokemon - chase it
            return FollowBehaviour(
                speed_multiplier=2.0, min_distance=10
            ).get_intended_move(entity, update_context)
        else:
            # No target - follow player
            return WanderFollowBehaviour(
                speed_multiplier=0.5, min_distance=30
            ).get_intended_move(entity, update_context)

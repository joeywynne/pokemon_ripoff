from enum import Enum, auto

from src.behaviours.behaviour import (
    EntityTargetingSystem,
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

    def __init__(
            self,
            follow_speed_multiplier=2.0,
            min_distance=50,
            stop_targeting_distance=150,
            start_targeting_distance=100):
        self.wander = WanderBehaviour(allow_stationary=False)
        
        follow_targeting = NearestTargeting(
            start_targeting_distance=start_targeting_distance,
            stop_targeting_distance=stop_targeting_distance
        )
        self.follow = FollowBehaviour(
            targeting_system=follow_targeting,
            speed_multiplier=follow_speed_multiplier,
            min_distance=min_distance,
        )

    def get_intended_move(self, entity, update_context):
        target = self.follow.select_target(entity, update_context)
        if target is not None:
            return self.follow.move_towards_target(entity, target)
        return self.wander.get_intended_move(entity, update_context)


class WanderFleeBehaviour(MovementBehaviour):

    def __init__(self, flee_speed_multiplier=2.0):
        flee_targeting = NearestTargeting(
            start_targeting_distance=100, stop_targeting_distance=150
        )
        self.flee = FleeBehaviour(speed_multiplier=flee_speed_multiplier, targeting_system=flee_targeting)
        self.wander = WanderBehaviour()
        
    def get_intended_move(self, entity, update_context):
        target = self.flee.select_target(entity, update_context)
        if target is not None:
            return self.flee.move_away_from_target(entity, target)
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
        follow_player_speed_mult: float = 0.5,
        wander_min_distance: int = 30,
        follow_speed_mult: float = 2.0,
        follow_min_distance: int = 10,
    ):
        self.follow_player = WanderFollowBehaviour(
            follow_speed_multiplier=follow_player_speed_mult, min_distance=wander_min_distance
        )
        self.attack = FollowBehaviour(
            speed_multiplier=follow_speed_mult,
            min_distance=follow_min_distance,
            targeting_system=EntityTargetingSystem()
        )
        self.attack_target = None

    def get_intended_move(self, entity, update_context) -> tuple[float, float]:
        if self.attack_target:
            # Target is Pokemon - chase it
            return self.attack.get_intended_move(entity, self.attack_target)
        else:
            # No target - follow player
            return self.follow_player.get_intended_move(entity, update_context)

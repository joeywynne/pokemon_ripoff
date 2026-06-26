from src.behaviours.behaviour import (
    MovementBehaviour,
    WanderBehaviour,
    StationaryBehaviour,
    FleeBehaviour,
    FollowBehaviour,
    TeleportBehaviour,
)
import random


class StationaryWanderBehaviour(MovementBehaviour):

    def __init__(self):
        self.wander = WanderBehaviour()
        self.idle = StationaryBehaviour()

        self.state = "wander"
        self.timer = random.randint(120, 300)

    def get_intended_move(self, entity, update_context):

        self.timer -= 1

        if self.timer <= 0:

            self.state = "idle" if self.state == "wander" else "wander"

            self.timer = random.randint(120, 300)

        if self.state == "wander":
            return self.wander.get_intended_move(entity, update_context)

        return self.idle.get_intended_move(entity, update_context)


class WanderFollowBehaviour(MovementBehaviour):

    def __init__(
        self, start_follow_distance=100, stop_follow_distance=150, speed_multiplier=3.0
    ):
        self.wander = WanderBehaviour()
        self.follow = FollowBehaviour(
            previous_behaviour=self.wander, speed_multiplier=speed_multiplier
        )

        self.state = "wander"
        self.start_follow_distance = start_follow_distance
        self.stop_follow_distance = stop_follow_distance

    def get_intended_move(self, entity, update_context):
        player_position = update_context.player_position
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.start_follow_distance:
            self.state = "follow"
        elif distance > self.stop_follow_distance:
            self.state = "wander"

        if self.state == "wander":
            return self.wander.get_intended_move(entity, update_context)
        return self.follow.get_intended_move(entity, update_context)


class WanderFleeBehaviour(MovementBehaviour):

    def __init__(
        self, start_flee_distance=100, stop_flee_distance=150, speed_multiplier=3.0
    ):
        self.wander = WanderBehaviour()
        self.flee = FleeBehaviour(
            previous_behaviour=self.wander, speed_multiplier=speed_multiplier
        )

        self.state = "wander"
        self.start_flee_distance = start_flee_distance
        self.stop_flee_distance = stop_flee_distance

    def get_intended_move(self, entity, update_context):
        player_position = update_context.player_position
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.start_flee_distance:
            self.state = "flee"
        elif distance > self.stop_flee_distance:
            self.state = "wander"

        if self.state == "wander":
            return self.wander.get_intended_move(entity, update_context)
        return self.flee.get_intended_move(entity, update_context)


class StationaryTeleportBehaviour(MovementBehaviour):

    def __init__(self, teleport_distance=150):
        self.state = "stationary"
        self.idle = StationaryBehaviour()
        self.teleport = TeleportBehaviour()
        self.teleport_frac = 1.0
        self.teleport_distance = teleport_distance

    def get_intended_move(self, entity, update_context):
        player_position = update_context.player_position
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.teleport_distance or self.state == "teleport":
            self.state = "teleport"
            self.teleport_frac -= 0.01
        else:
            self.state = "stationary"

        if self.state == "teleport":
            dx, dy = self.teleport.get_intended_move(entity, update_context)

        else:
            dx, dy = self.idle.get_intended_move(entity, update_context)

        if self.teleport_frac <= 0:
            self.teleport_frac = 1.0
            self.state = "stationary"

        return dx, dy

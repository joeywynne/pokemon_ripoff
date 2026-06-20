from src.movement.behaviour import MovementBehaviour, WanderBehaviour, StationaryBehaviour, FollowBehaviour
import random


class StationaryWanderBehaviour(MovementBehaviour):

    def __init__(self):
        self.wander = WanderBehaviour()
        self.idle = StationaryBehaviour()

        self.state = "wander"
        self.timer = random.randint(120, 300)

    def get_intended_move(self, entity, **kwargs):

        self.timer -= 1

        if self.timer <= 0:

            self.state = (
                "idle"
                if self.state == "wander"
                else "wander"
            )

            self.timer = random.randint(120, 300)

        if self.state == "wander":
            return self.wander.get_intended_move(
                entity,
                **kwargs,
            )

        return self.idle.get_intended_move(
            entity,
            **kwargs,
        )



class WanderFollowBehaviour(MovementBehaviour):

    def __init__(self, start_follow_distance=100, stop_follow_distance=150):
        self.wander = WanderBehaviour()
        self.follow = FollowBehaviour()

        self.state = "wander"
        self.start_follow_distance = start_follow_distance
        self.stop_follow_distance = stop_follow_distance

    def get_intended_move(self, entity, player_position: tuple[float, float]):
        dx = player_position[0] - entity.x
        dy = player_position[1] - entity.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.start_follow_distance:
            self.state = "follow"
        elif distance > self.stop_follow_distance:
            self.state = "wander"

        if self.state == "wander":
            return self.wander.get_intended_move(entity)
        return self.follow.get_intended_move(entity, player_position, speed_multiplier=2)


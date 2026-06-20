from src.movement.behaviour import MovementBehaviour, WanderBehaviour, StationaryBehaviour
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
    


from src.behaviours.composite_behaviours import (
    StationaryWanderBehaviour,
    StationaryTeleportBehaviour,
    WanderFollowBehaviour,
    WanderFleeBehaviour,
)
from src.behaviours.behaviour import (
    PlayerBehaviour,
    PokeballBehaviour,
    StationaryBehaviour,
    PacingBehaviour,
    FollowBehaviour,
    FleeBehaviour,
    TeleportBehaviour,
)

BEHAVIOUR_FACTORIES = {
    "player": PlayerBehaviour,
    "pokeball": PokeballBehaviour,
    "stationary": StationaryBehaviour,
    "pacing": PacingBehaviour,
    "follow": FollowBehaviour,
    "flee": FleeBehaviour,
    "teleport": TeleportBehaviour,
    "stationary_wander": StationaryWanderBehaviour,
    "stationary_teleport": StationaryTeleportBehaviour,
    "wander_follow": WanderFollowBehaviour,
    "wander_flee": WanderFleeBehaviour,
}

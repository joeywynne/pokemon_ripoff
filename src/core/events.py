from dataclasses import dataclass, field
from src.entities.pokemon import Pokemon

class GameEvent:
    pass

@dataclass
class PokemonCapturedEvent(GameEvent):
    pokemon: Pokemon

@dataclass
class EventQueue:
    events: list[GameEvent] = field(default_factory=list)

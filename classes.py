from dataclasses import dataclass
from typing import Literal


@dataclass
class Module:
    name: Literal['productivity-module-1', 'productivity-module-2', 'productivity-module-3', 'speed-module-1', 'speed-module-2', 'speed-module-3']
    productivity: float
    speed: float

@dataclass
class Machine:
    name: str
    slots: int
    speed: float
    productivity: float  #TODO??????????????

@dataclass
class EffectedMachine(Machine):
    speedInGame: float = 0
    def __init__(self, machine: Machine):
        self.name = machine.name
        self.slots = machine.slots
        self.speed = machine.speed
        self.productivity = machine.productivity

@dataclass
class Effect:
    speed: float = 0.0
    productivity: float = 0.0

@dataclass
class Item:
    name: str
    elementary: bool
    image: str
    production_time: float
    quantity: float
    recipe: dict[str, float]

    @property
    def frequency(self) -> str | None:
        if (self.elementary): return
        return self.quantity / self.production_time

@dataclass
class ItemMeta:
    item: Item
    amount: float | None = None
    machinesAmount: float | None = None
    speed: float | None = None
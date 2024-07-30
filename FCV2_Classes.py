from dataclasses import dataclass
from typing import Literal


@dataclass
class Module:
    name: Literal['productivity-module-1', 'productivity-module-2', 'productivity-module-3', 'speed-module-1', 'speed-module-2', 'speed-module-3']
    productivity: float
    speed: float

PRODUCTIVITY_MODULE_1 = Module('productivity-module-1', 0.04, -0.05)
PRODUCTIVITY_MODULE_2 = Module('productivity-module-2', 0.06, -0.1)
PRODUCTIVITY_MODULE_3 = Module('productivity-module-3', 0.1, -0.15)

SPEED_MODULE_1 = Module('speed-module-1', 0.0, 0.2)
SPEED_MODULE_2 = Module('speed-module-2', 0.0, 0.3)
SPEED_MODULE_3 = Module('speed-module-3', 0.0, 0.5)

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


ASSENBLING_MACHINE_1 = Machine('assembling-machine-1', 0, 0.5, 0)
ASSENBLING_MACHINE_2 = Machine('assembling-machine-2', 2, 0.75, 0)
ASSENBLING_MACHINE_3 = Machine('assembling-machine-3', 4, 1.25, 0)

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

@dataclass
class ItemMeta:
    item: Item
    amount: float | None = None
    machinesAmount: float | None = None
    speed: float | None = None
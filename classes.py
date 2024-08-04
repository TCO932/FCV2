import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Literal


@dataclass
class Module:
    name: Literal['productivity-module-1', 'productivity-module-2', 'productivity-module-3', 'speed-module-1', 'speed-module-2', 'speed-module-3']
    productivity: float
    speed: float

MACHINE_TYPES = ['assembling-machine', 'furnace', 'oil-refinery', 'chemical-plant', 'centrifuge', 'lab', 'rocket-silo']

class MachineType(Enum):
    ASSEMBLING_MACHINE = auto()
    FURNACE = auto()
    OIL_REFINERY = auto()
    CHEMICAL_PLANT = auto()
    CENTRIFUGE = auto()
    LAB = auto()
    ROCKET_SILO = auto()

@dataclass
class Machine():
    name: str
    slots: int
    speed: float
    productivity: float
    type: Literal['assembling-machine', 'furnace', 'oil-refinery', 'chemical-plant', 'centrifuge', 'lab', 'rocket-silo'] =  'assembling-machine'

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

    def __str__(self):
        return (f"Item(name={self.name}, elementary={self.elementary}, "
                f"image={self.image}, production_time={self.production_time}, "
                f"quantity={self.quantity}, recipe={self.recipe})")

@dataclass
class ItemMeta(Item):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    amount: float | None = None
    machine: Machine | None = None
    machinesAmount: float | None = None
    speed: float | None = None

    def __len__(self):
        return len(vars(self))

    def __eq__(self, other):
        return isinstance(other, ItemMeta) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return (f"ItemMeta(id={self.id}, name={self.name}, elementary={self.elementary}, "
                f"image={self.image}, production_time={self.production_time}, "
                f"quantity={self.quantity}, recipe={self.recipe}, "
                f"amount={self.amount}, machine={self.machine}, "
                f"machinesAmount={self.machinesAmount}, speed={self.speed})")


@dataclass
class ItemTree():
    nodes: set[ItemMeta] = field(default_factory=set)
    links: dict[str, list[str]] = field(default_factory=dict)
    root: str | None = None

    def addRoot(self, node: ItemMeta) -> str:
        self.nodes.add(node)
        self.root = node.id
        return self.root

    def addNode(self, node: ItemMeta, parentId: str):
        if node in self.nodes:
            return

        self.nodes.add(node)
        if parentId in self.links:
            self.links[parentId].append(node.id)

    def getNode(self, id: str):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def __getitem__(self, node_id: str) -> ItemMeta | None:
        return self.getNode(node_id)

    def updateNode(self, nodeId: str, node: ItemMeta):
        pass

    def _deleteDeepLink(self, nodeId: str):
        children = self.children(nodeId)

        for child in children:
            self._deleteDeepLink(child)

        del self.links[nodeId]

    def deleteNode(self, node: ItemMeta):
        parentId = self.parent(node)
        if parentId:
            self.links[parentId].remove(node.id)

        self._deleteDeepLink(node.id)

        self.nodes.remove(node)

    def children(self, parentNodeId: str) -> list[str]:
        return self.links.get(parentNodeId, [])

    def parent(self, node: ItemMeta) -> str | None:
        for parentId, children in self.links.items():
            if node.id in children:
                return parentId
        return None

    
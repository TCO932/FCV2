import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Literal, Optional, Protocol


class FormattedNameProtocol(Protocol):
    name: str
    def getFormattedName(self):
        return self.name.replace('-', ' ').title()

@dataclass(frozen=True)
class Module(FormattedNameProtocol):
    name: Literal['productivity-module-1', 'productivity-module-2', 'productivity-module-3', 'speed-module-1', 'speed-module-2', 'speed-module-3']
    productivity: float
    speed: float

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Module):
            return self.name == other.name
        return False

class ModulesDict(dict[
    Literal['productivity-module-1', 'productivity-module-2', 'productivity-module-3', 'speed-module-1', 'speed-module-2', 'speed-module-3'],
    int
]):
    pass

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
class Machine(FormattedNameProtocol):
    name: str
    slots: int
    basicSpeed: float
    basicProductivity: float
    maxBeacons: int
    type: Literal['assembling-machine', 'furnace', 'oil-refinery', 'chemical-plant', 'centrifuge', 'lab', 'rocket-silo'] =  'assembling-machine'

    def __str__(self):
        return (f"Machine(name={self.name}, "
                f"slots={self.slots}, "
                f"speed={self.basicSpeed}, "
                f"productivity={self.basicProductivity}, "
                f"maxBeacons={self.maxBeacons}, "
                f"type={self.type})")

@dataclass
class EffectedMachine(Machine):
    modules: dict[Module: int] = field(default_factory=dict)
    beaconsNumber: int = 0

    @classmethod
    def fromMachine(cls, machine: Machine, **kargs):
        EffectedMachine = vars(machine)
        EffectedMachine.update(kargs)
        return cls(**EffectedMachine)

    @property
    def productivity(self) -> float:
        productivity = self.basicProductivity
        for module, amount in self.modules.items():
            productivity += module.productivity * amount
        return productivity

    @property
    def speedNoProd(self) -> float:
        speed = self.basicSpeed
        modulesSpeed = 0
        for module, amount in self.modules.items():
            modulesSpeed += module.speed * amount

        speed = speed * (1 + modulesSpeed + self.beaconsNumber*0.5)
        return speed

    @property
    def speed(self) -> float:
        return self.speedNoProd * (1 + self.productivity)


@dataclass
class Item:
    name: str
    elementary: bool
    image: str
    production_time: float
    quantity: float
    recipe: dict[str, float]
    machineType: Literal['assembling-machine', 'furnace', 'oil-refinery', 'chemical-plant', 'centrifuge', 'lab', 'rocket-silo', 'mining-drill'] | None
    no_prod: bool = False

    def __str__(self):
        return (f"Item(name={self.name}, elementary={self.elementary}, "
                f"image={self.image}, production_time={self.production_time}, "
                f"quantity={self.quantity}, recipe={self.recipe}, no_prod={self.no_prod})")

@dataclass
class ItemMeta(Item):
    id: str =''
    amount: float | None = None
    effectedMachine: EffectedMachine | None = None
    speed: float | None = None

    @property
    def machinesAmount(self) -> float | None:
        if self.elementary or (not self.effectedMachine):
            return None 
        else:
            return (self.speed*self.production_time) / (self.quantity*self.effectedMachine.speed)

    def __init__(self, **kargs):
        # Извлекаем аргументы, относящиеся к Item
        item_args = {key: kargs[key] for key in Item.__dataclass_fields__ if key in kargs}
        super().__init__(**item_args)  # Вызов конструктора родительского класса
        # Устанавливаем оставшиеся аргументы для ItemMeta
        for key, value in kargs.items():
            if key not in Item.__dataclass_fields__:
                setattr(self, key, value)
        self.id = str(uuid.uuid4())


    @classmethod
    def fromItem(cls, item: Item, **kargs):
        item_data = vars(item)
        item_data.update(kargs)
        return cls(**item_data)

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
                f"amount={self.amount}, machine={self.effectedMachine}, "
                f"machinesAmount={self.machinesAmount}, speed={self.speed})")


@dataclass
class ItemTree():
    nodes: dict[str, ItemMeta] = field(default_factory=dict)
    links: dict[str, list[str]] = field(default_factory=dict)
    root: str | None = None

    def addRoot(self, node: ItemMeta) -> str:
        self.nodes[node.id] = node
        self.root = node.id
        return self.root

    def addNode(self, node: ItemMeta, parentId: str):
        if node in self.nodes:
            return

        if parentId is None:
            self.addRoot(node)

        self.nodes[node.id] = node
        self.addLink(node, parentId)

    def addLink(self, node: ItemMeta, parentId: str):
        if parentId in self.nodes:
            if parentId in self.links:
                self.links[parentId].append(node.id)
            else:
                self.links[parentId] = [node.id]

    def replaceNodeWithSubTree(self, node: ItemMeta, subTree: 'ItemTree') -> Optional['ItemTree']:
        parentId = self.parent(node)
        if parentId is None: 
            return None

        rootNode = subTree.getNode(subTree.root)

        self.addLink(rootNode, parentId)
        self.deleteNode(node)
        self.nodes.update(subTree.nodes)
        self.links.update(subTree.links)

        return self

    def getNode(self, nodeId: str):
        for id, node in self.nodes.items():
            if nodeId == id:
                return node
        return None

    def __getitem__(self, node_id: str) -> ItemMeta | None:
        return self.getNode(node_id)

    def updateNode(self, nodeId: str, node: ItemMeta):
        pass

    def __deleteDeep(self, nodeId: str):
        children = self.children(nodeId)

        for child in children:
            self.__deleteDeep(child)

        self.nodes.pop(nodeId)

        if nodeId in self.links:
            del self.links[nodeId]

    def deleteNode(self, node: ItemMeta):
        parentId = self.parent(node)
        if parentId:
            self.links[parentId].remove(node.id)

        self.__deleteDeep(node.id)


    def children(self, parentNodeId: str) -> list[str]:
        return self.links.get(parentNodeId, [])

    def parent(self, node: ItemMeta) -> str | None:
        for parentId, children in self.links.items():
            if node.id in children:
                return parentId
        return None

if __name__ == "__main__":
    PRODUCTIVITY_MODULE_1 = Module('productivity-module-1', 0.04, -0.05)
    PRODUCTIVITY_MODULE_2 = Module('productivity-module-2', 0.06, -0.1)
    PRODUCTIVITY_MODULE_3 = Module('productivity-module-3', 0.1, -0.15)

    SPEED_MODULE_1 = Module('speed-module-1', 0.0, 0.2)
    SPEED_MODULE_2 = Module('speed-module-2', 0.0, 0.3)
    SPEED_MODULE_3 = Module('speed-module-3', 0.0, 0.5)

    MODULES = {
        'productivity-module-1': PRODUCTIVITY_MODULE_1,
        'productivity-module-2': PRODUCTIVITY_MODULE_2,
        'productivity-module-3': PRODUCTIVITY_MODULE_3,
        'speed-module-1': SPEED_MODULE_1,
        'speed-module-2': SPEED_MODULE_2,
        'speed-module-3': SPEED_MODULE_3,
    }

    ASSENBLING_MACHINE_1 = Machine('assembling-machine-1', 0, 0.5, 0, 12,)
    ASSENBLING_MACHINE_2 = Machine('assembling-machine-2', 2, 0.75, 0, 12,)
    ASSENBLING_MACHINE_3 = Machine('assembling-machine-3', 4, 1.25, 0, 12,)
    ELECTRIC_FURNACE = Machine('electric-furnace', 2, 2, 0, 12, 'furnace')
    OIL_REFINERY = Machine('oil-refinery', 3, 1, 0, 16, 'oil-refinery')
    CHEMICAL_PLANT = Machine('chemical-plant', 3, 1, 0, 12, 'chemical-plant')
    CENTRIFUGE = Machine('centrifuge', 2, 2, 0, 12, 'centrifuge')
    LAB = Machine('lab', 2, 1, 0, 12, 'lab')
    LAB_MAX_SPEED = Machine('lab', 2, 1.5, 0, 12, 'lab')
    ROCKET_SILO = Machine('rocket-silo', 4, 1, 0, 20, 'rocket-silo')

    MACHINES = {
        'assembling-machine-1': ASSENBLING_MACHINE_1,
        'assembling-machine-2': ASSENBLING_MACHINE_2,
        'assembling-machine-3': ASSENBLING_MACHINE_3,
        'electric-furnace': ELECTRIC_FURNACE,
        'oil-refinery': OIL_REFINERY,
        'chemical-plant': CHEMICAL_PLANT,
        'centrifuge': CENTRIFUGE,
        'lab': LAB,
        'lab': LAB_MAX_SPEED,
        'rocket-silo': ROCKET_SILO,
    }

    ASSENBLING_MACHINES = {
        'assembling-machine-1': ASSENBLING_MACHINE_1, 
        'assembling-machine-2': ASSENBLING_MACHINE_2, 
        'assembling-machine-3': ASSENBLING_MACHINE_3, 
    }

    ITEMS = {
        'advanced-circuit': Item(
            name='advanced-circuit',
            elementary=False,
            image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/advanced-circuit.png',
            production_time=6,
            quantity=1,
            recipe={'copper-cable': 4, 'electronic-circuit': 2, 'plastic-bar': 2}
        ),
        'automation-science-pack': Item(
            name='automation-science-pack',
            elementary=False,
            image='https://raw.githubusercontent.com/TCO932/Factorio-Calculator-App/master/images/automation-science-pack.png',
            production_time=5,
            quantity=1,
            recipe={'copper-plate': 1, 'iron-gear-wheel': 1}
        ),
    }

    modules = {PRODUCTIVITY_MODULE_3: 4}
    itemMeta = ItemMeta.fromItem(
        ITEMS.get('advanced-circuit'),
        effectedMachine=EffectedMachine.fromMachine(
            ASSENBLING_MACHINE_3, 
            modules=modules, 
            beaconsNumber=12
        )
    )
    itemMeta
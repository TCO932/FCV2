from typing import Literal, Optional

from diskcache import Cache
from treelib import Node, Tree

from classes import *
from consts import *
from data import *

cache = Cache('cache')

def calcEffect(effects: dict[int: Module], beaconsAmount: int) -> Effect:
    resEffect = Effect(
        speed=beaconsAmount*SPEED_MODULE_3.speed/2
    )
    for moduleName, amount in effects.items():
        module = MODULES[moduleName]
        resEffect.productivity += module.productivity * amount
        resEffect.speed += module.speed * amount
    return resEffect
    
def setEffects(machine: Machine, effects: dict[str: int], beaconsAmount: int) -> EffectedMachine:
    effectedMachine = EffectedMachine.fromMachine(machine)
    
    effect = calcEffect(effects, beaconsAmount)

    effectedMachine.productivity = effect.productivity
    effectedMachine.speed = machine.speed * (1 + effect.speed) * (1 + effect.productivity)
    effectedMachine.speedInGame = machine.speed * (1 + effect.speed)

    return effectedMachine

@cache.memoize()
def buildCraftTree(itemName: str, amount: float, machine: Machine, craftTree: Tree = None) -> Tree:
    craftTree = craftTree if craftTree is not None else Tree()
    def buildNode(itemName: str, amount: float, machine: Machine, root: Optional[str] = None):
        item = RECIPES.get(itemName)

        if (item == None): return
        node = Node(itemName, data=ItemMeta(**vars(item), amount=amount)) #TODO SPEED
        craftTree.add_node(node, root)

        if (item.elementary): return

        for componentName, componentAmount in item.recipe.items():
            component = RECIPES.get(componentName)
            prodModifier = machine.productivity
            quantityModifier = component.quantity if component.quantity > 0 else 1
            amountModifier = quantityModifier * (1 + prodModifier)
            buildNode(componentName, componentAmount*amount / amountModifier, machine, node.identifier)

    buildNode(itemName, amount, machine)

    return craftTree

def calcRes(craftTree: Tree):
    res: dict[str: float] = {}

    for node in craftTree.all_nodes():
        itemName = node.tag
        amount = node.data.amount

        if itemName in res:
            res[itemName] += amount
        else:
            res[itemName] = amount

    return res

def craftTreeWithAmounts(craftTree: Tree) -> Tree:
    tree = Tree(craftTree.subtree(craftTree.root), deep=True)

    for nodeName in craftTree.expand_tree():
        node = tree[nodeName]
        node.tag = node.tag + ' x{}'.format(node.data.amount)

    return tree

def buildSpeedTree(itemName:str, itemPerSecond: float, machine: Machine, craftTree: Tree = Tree()) -> Tree:
    def buildSpeedNode(itemName: str, itemPerSecond: float, machine: Machine, root: Optional[str] = None):
        item = RECIPES.get(itemName)

        if (item == None): return

        machinesAmount = None if item.elementary else (itemPerSecond*item.production_time) / (item.quantity*machine.speed)
        node = Node(itemName, data=ItemMeta(**vars(item),  speed=itemPerSecond, machinesAmount=machinesAmount)) #TODO SPEED

        craftTree.add_node(node, root)

        if (item.elementary): return

        for componentName, componentAmount in item.recipe.items():
            component = RECIPES.get(componentName)
            prodModifier = machine.productivity
            quantityModifier = component.quantity if component.quantity > 0 else 1 #TODO fix
            amountModifier = quantityModifier * (1 + prodModifier)

            buildSpeedNode(componentName, componentAmount*itemPerSecond/amountModifier, machine, node.identifier)

    buildSpeedNode(itemName, itemPerSecond, machine)

    return craftTree

def calcMachinesAmount(itemMeta: ItemMeta) -> float | None:
    return None if itemMeta.elementary else (itemMeta.speed*itemMeta.production_time) / (itemMeta.quantity*itemMeta.machine.speed)


def initSpeedTree(itemMeta: ItemMeta, itemTree: ItemTree | None = None) -> ItemTree:
    itemTree = itemTree if itemTree else ItemTree()

    itemMeta.machinesAmount = calcMachinesAmount(itemMeta)
    itemTree.addRoot(itemMeta)

    return itemTree


def buildChildrenSpeed(itemMeta: ItemMeta, machine: Machine, tree: ItemTree) -> ItemTree:
    for childName, amount in itemMeta.recipe.items():
        childItem: Item = RECIPES[childName]
        childItemSpeed = itemMeta.speed * amount
        childItemMeta = ItemMeta.fromItem(childItem, machine=ASSENBLING_MACHINE_3, speed=childItemSpeed)
        childItemMeta.machinesAmount = calcMachinesAmount(childItem)
        tree.addNode(childItemMeta, itemMeta.id)

    return tree


def craftTreeWithSpeeds(craftTree: Tree) -> Tree:
    tree = Tree(craftTree.subtree(craftTree.root), deep=True)

    for nodeName in craftTree.expand_tree():
        node = tree[nodeName]
        tag = node.tag + ' x{}(i/s)'.format(node.data.speed)
        if (not node.data.elementary):
            tag +=  ' {}m'.format(node.data.machinesAmount)
        node.tag = tag

    return tree

if __name__ == "__main__":
    effectedMachine = setEffects(None, None, 'FULL')
    print(effectedMachine)

    tree = buildCraftTree('rocket-part', 100, ASSENBLING_MACHINE_3)
    # print(tree)


    res = calcRes(tree)
    print(res)

    aTree = craftTreeWithAmounts(tree)
    print(aTree)
    sTree = buildSpeedTree('electric-engine-unit', 1, ASSENBLING_MACHINE_3)
    print(sTree)
    saTree = craftTreeWithSpeeds(sTree)
    print(saTree)

# tree = Tree()
# node1 = Node("Harry", "harry")  # root node
# tree.add_node(node1, None)
# node1 = Node("Potter", "potter")
# tree.add_node(node1, 'harry')
# tree.show(line_type='ascii')
# byte_string = b'Harry\n+-- Potter\n'

# # Декодирование байтовой строки
# decoded_string = byte_string.decode('utf-8')

# # Вывод результата
# print(decoded_string)
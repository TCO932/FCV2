from typing import Literal, Optional
from classes import *
from utility import *
from data import *
from consts import *
from treelib import Node, Tree
from diskcache import Cache

cache = Cache('cache')

def calcEffect(effects: dict[int: Module]) -> Effect:
    resEffect = Effect()
    for amount, module in effects.items():
        resEffect.productivity += module.productivity * amount
        resEffect.speed += module.speed * amount
    return resEffect
    
def setEffects(machine: Machine, effects: dict[Module: int], mode: Literal['FULL', 'ONLY_PROD', 'CUSTOM'] = 'CUSTOM') -> EffectedMachine:
    """
    FULL (max amount beacons with 2 tier 3 speed modules, max amount tier 3 prod modules); 

    ONLY_PROD (max amount tier 3 prod modules);

    CUSTOM (default value, custom beacons and speed modules amount, custom speed module tiers)
    """

    def FullMode():
        machine = ASSENBLING_MACHINE_3
        effects: dict[int: Module] = {
            machine.slots: PRODUCTIVITY_MODULE_3, 12: SPEED_MODULE_3 #TODO: fix 12 in future
        }
        effectedMachine = EffectedMachine(machine)
        effect = calcEffect(effects)
        effectedMachine.productivity = effect.productivity
        effectedMachine.speedInGame = machine.speed * (1 + effect.speed)
        effectedMachine.speed = machine.speed * (1 + effect.speed) * (1 + effect.productivity) #TODO: check this in game

        return effectedMachine

    def customMode():

        return 

    switcher = {}
    switcher['FULL'] = FullMode
    switcher['ONLY_PROD'] = customMode
    switcher['CUSTOM'] = customMode

    def switch_case(case):
        return switcher.get(case, lambda: customMode)()

    return switch_case(mode)

@cache.memoize()
def buildCraftTree(itemName: str, amount: float, machine: Machine, craftTree: Tree = Tree()) -> Tree:
    def buildNode(itemName: str, amount: float, machine: Machine, root: Optional[str] = None):
        item = RECIPES.get(itemName)

        if (item == None): return
        node = Node(itemName, data=ItemMeta(item, amount=amount)) #TODO SPEED
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
        node = Node(itemName, data=ItemMeta(item,  speed=itemPerSecond, machinesAmount=machinesAmount)) #TODO SPEED

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

def craftTreeWithSpeeds(craftTree: Tree) -> Tree:
    tree = Tree(craftTree.subtree(craftTree.root), deep=True)

    for nodeName in craftTree.expand_tree():
        node = tree[nodeName]
        tag = node.tag + ' x{}(i/s)'.format(node.data.speed)
        if (not node.data.item.elementary):
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
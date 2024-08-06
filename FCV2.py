import time
from typing import Literal, Optional

from diskcache import Cache
from treelib import Node, Tree

from classes import *
from consts import *
from data import *

cache = Cache('cache')

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Время начала
        result = func(*args, **kwargs)     # Вызов оригинальной функции
        end_time = time.perf_counter()      # Время окончания
        duration = end_time - start_time    # Длительность выполнения
        print(f"Длительность работы функции '{func.__name__}': {duration:.6f} секунд")
        return result                       # Возврат результата оригинальной функции
    return wrapper

@cache.memoize(expire=3600)
def buildCraftTree(itemName: str, amount: float, machine: Machine, craftTree: Tree = None) -> Tree:
    craftTree = craftTree if craftTree is not None else Tree()
    def buildNode(itemName: str, amount: float, machine: Machine, root: Optional[str] = None):
        item = ITEMS.get(itemName)

        if (item == None): return
        node = Node(itemName, data=ItemMeta(**vars(item), amount=amount)) #TODO SPEED
        craftTree.add_node(node, root)

        if (item.elementary): return

        for componentName, componentAmount in item.recipe.items():
            component = ITEMS.get(componentName)
            prodModifier = machine.basicProductivity
            quantityModifier = component.quantity if component.quantity > 0 else 1
            amountModifier = quantityModifier * (1 + prodModifier)
            buildNode(componentName, componentAmount*amount / amountModifier, machine, node.identifier)

    buildNode(itemName, amount, machine)

    return craftTree

# old
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

# old
def craftTreeWithAmounts(craftTree: Tree) -> Tree:
    tree = Tree(craftTree.subtree(craftTree.root), deep=True)

    for nodeName in craftTree.expand_tree():
        node = tree[nodeName]
        node.tag = node.tag + ' x{}'.format(node.data.amount)

    return tree

@cache.memoize(expire=3600)
@time_it
def buildSpeedTree(itemMeta: ItemMeta) -> ItemTree:
    def buildSpeedNode(itemMeta: ItemMeta, parentId: Optional[str] = None):
        itemTree.addNode(itemMeta, parentId)

        if (itemMeta.elementary): return

        for componentName, componentAmount in itemMeta.recipe.items():
            componentMeta = ItemMeta.fromItem(
                ITEMS.get(componentName), 
                effectedMachine=itemMeta.effectedMachine, 
            )
            prodModifier = itemMeta.effectedMachine.productivity
            quantityModifier = componentMeta.quantity if componentMeta.quantity > 0 else 1 #TODO fix
            amountModifier = quantityModifier * (1 + prodModifier)
            componentMeta.speed = componentAmount*itemMeta.speed/amountModifier
            buildSpeedNode(componentMeta, itemMeta.id)

    itemTree = ItemTree()
    buildSpeedNode(itemMeta)

    return itemTree


def initSpeedTree(itemMeta: ItemMeta, itemTree: ItemTree | None = None) -> ItemTree:
    itemTree = itemTree if itemTree else ItemTree()

    itemTree.addRoot(itemMeta)

    return itemTree


def buildChildrenSpeed(itemMeta: ItemMeta, tree: ItemTree) -> ItemTree:
    for childName, amount in itemMeta.recipe.items():
        childItem: Item = ITEMS[childName]
        childItemMeta = ItemMeta.fromItem(
            childItem, 
            effectedMachine=EffectedMachine.fromMachine(ASSENBLING_MACHINE_3), 
            speed=itemMeta.speed * amount
        )
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
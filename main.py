import sys
import time

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication

import FCV2 as fcv2
from classes import EffectedMachine, ItemMeta, ItemTree
from data import *
from widgets.Graph import GraphView, Node
from widgets.ItemsListTable import ItemsListTableView
from widgets.ItemTable import ItemTableView
from widgets.MachineWidget import MachineWidget
from widgets.MainWindow import MainWindow


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Время начала
        result = func(*args, **kwargs)     # Вызов оригинальной функции
        end_time = time.perf_counter()      # Время окончания
        duration = end_time - start_time    # Длительность выполнения
        print(f"Длительность работы функции '{func.__name__}': {duration:.6f} секунд")
        return result                       # Возврат результата оригинальной функции
    return wrapper

global speedTree
speedTree = None
global item

def itemClickHandler(selectedItem: Item):
    global speedTree
    global item
    item = selectedItem
    itemMeta = ItemMeta.fromItem(
        item, 
        speed=1, 
        effectedMachine=EffectedMachine.fromMachine(
            ASSENBLING_MACHINE_1,
            modules=[],
            beaconsNumber=0
        )
    )
    tree = ItemTree()
    tree.addRoot(itemMeta)
    graphicsView.build_graph(tree)
    graphicsView.selectNode(itemMeta)

    mainWindow.tabWidget.setCurrentIndex(1)

def rootItemSpeedSettedHandler(speed: float):
    global speedTree
    global item
    itemMeta = ItemMeta.fromItem(
        item, 
        speed=speed, 
        effectedMachine=EffectedMachine.fromMachine(
            ASSENBLING_MACHINE_1,
            modules=[],
            beaconsNumber=0
        )
    )

    speedTree = fcv2.buildSpeedTree(itemMeta)
    graphicsView.build_graph(speedTree)
    print(speed)

def buildTree(itemMeta: ItemMeta, effectedMachine: EffectedMachine):
    updTree = fcv2.buildChildrenSpeed(itemMeta, effectedMachine, speedTree)
    graphicsView.build_graph(updTree)

def nodeSelectioHandler(node: Node):
    itemTableView.setItem(node.itemMeta)
    machineWidget.setModel(node.itemMeta)

def machineSetHandler(effectedMachine: EffectedMachine):
    global speedTree
    currentItemMeta = itemTableView.itemMeta
    currentItemMeta.effectedMachine = effectedMachine
    if speedTree:
        fcv2.recalcSpeedSubtree(currentItemMeta, speedTree)
    else:
        speedTree = fcv2.buildSpeedTree(currentItemMeta)

    graphicsView.build_graph(speedTree)
    graphicsView.selectNode(currentItemMeta)
    print(currentItemMeta)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    machineWidget = MachineWidget()
    itemTableView = ItemTableView()
    itemsListTableView = ItemsListTableView(ITEMS)

    graphicsView = GraphView(itemTableView)
    mainWindow = MainWindow(itemsListTableView, graphicsView, itemTableView, machineWidget)

    itemsListTableView.itemClicked.connect(itemClickHandler)
    
    graphicsView.nodeSelected.connect(nodeSelectioHandler)
    
    machineWidget.machineSetted.connect(machineSetHandler)

    mainWindow.rootItemSpeedSetted.connect(rootItemSpeedSettedHandler)

    mainWindow.show()
    sys.exit(app.exec())

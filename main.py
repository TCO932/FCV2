import sys
import time

from PyQt6 import QtWidgets
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QApplication

import FCV2 as fcv2
from classes import EffectedMachine, ItemMeta, ItemTree
from data import *
from widgets.MainWindow import MainWindow
from widgets.Graph import GraphView, Node
from widgets.ItemsListTable import ItemsListTableView
from widgets.ItemTable import ItemTableView
from widgets.MachineWidget import MachineWidget


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

def itemClickHandler(item: Item):
    global speedTree
    itemMeta = ItemMeta.fromItem(
        item, 
        speed=0.1, 
        effectedMachine=EffectedMachine.fromMachine(
            ASSENBLING_MACHINE_3,
            modules=[PRODUCTIVITY_MODULE_3, PRODUCTIVITY_MODULE_3, PRODUCTIVITY_MODULE_3, PRODUCTIVITY_MODULE_3],
            beaconsNumber=12
        )
    )

    speedTree = fcv2.buildSpeedTree(itemMeta)
    graphicsView.build_graph(speedTree)
    graphicsView.selectNode(itemMeta)

    mainWindow.tabWidget.setCurrentIndex(1)

def buildTree(itemMeta: ItemMeta, effectedMachine: EffectedMachine):
    updTree = fcv2.buildChildrenSpeed(itemMeta, effectedMachine, speedTree)
    graphicsView.build_graph(updTree)

def nodeSelectioHandler(node: Node):
    print('node selected')
    itemTableView.setItem(node.itemMeta)
    machineWidget.setModel(node.itemMeta.effectedMachine)

def machineSetHandler(effectedMachine: EffectedMachine):
    global speedTree
    currentItemMeta = itemTableView.itemMeta
    currentItemMeta.effectedMachine = effectedMachine
    speedSubTree = fcv2.buildSpeedTree(currentItemMeta)
    speedTree.replaceNodeWithSubTree(currentItemMeta, speedSubTree)
    graphicsView.build_graph(speedTree)
    print(currentItemMeta)

def rootItemSpeedSettedHandler(speed: float):
    print(speed)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    machineWidget = MachineWidget()
    itemTableView = ItemTableView()
    itemsListTableView = ItemsListTableView(ITEMS)

    graphicsView = GraphView(itemTableView)
    mainWindow = MainWindow(window, itemsListTableView, graphicsView, itemTableView, machineWidget)

    itemsListTableView.itemClicked.connect(itemClickHandler)
    
    graphicsView.nodeSelected.connect(nodeSelectioHandler)
    
    machineWidget.machineSetted.connect(machineSetHandler)

    mainWindow.rootItemSpeedSetted.connect(rootItemSpeedSettedHandler)

    mainWindow.show()
    sys.exit(app.exec())

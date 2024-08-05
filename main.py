import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QApplication

import FCV2 as fcv2
from classes import ItemMeta, ItemTree, EffectedMachine
from data import *
from qtUI.Tabs_ui import Ui_MainWindow
from widgets.Graph import GraphView, Node
from widgets.ItemsListTable import ItemsListTableView
from widgets.ItemTable import ItemTableView
from widgets.MachineWidget import MachineWidget, MachineWidgetModel


speedTree

def itemClickHandler(item: Item):
    global speedTree
    itemMeta: ItemMeta = ItemMeta.fromItem(item)
    itemMeta = ItemMeta.fromItem(item, speed=1, machine=ASSENBLING_MACHINE_3)

    speedTree = fcv2.initSpeedTree(itemMeta)
    graphicsView.build_graph(speedTree)
    itemTableView.setItem(itemMeta)
    graphicsView.selectNode(itemMeta)
    ui.tabWidget.setCurrentIndex(1)

def buildTree(machineWidgetModel: MachineWidgetModel, itemMeta: ItemMeta):
    effectedMachine = fcv2.setEffects(
        machine=machineWidgetModel.machine,
        effects={machineWidgetModel.module.name: machineWidgetModel.modulesNumber},
        beaconsAmount=machineWidgetModel.beaconsNumber
    )
    updTree = fcv2.buildChildrenSpeed(itemMeta, effectedMachine, speedTree)
    graphicsView.build_graph(updTree)

def nodeSelectioHandler(node: Node):
    print('node selected')
    itemTableView.setItem(node.itemMeta)

def calculateClickHandler(machineWidgetModel: MachineWidgetModel):
    currentItemMeta = itemTableView.itemMeta

    buildTree(machineWidgetModel, currentItemMeta)
    print(currentItemMeta)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    machineWidget = MachineWidget()
    itemTableView = ItemTableView()
    itemsListTableView = ItemsListTableView(RECIPES)

    graphicsView = GraphView(itemTableView)
    ui = Ui_MainWindow(itemsListTableView, graphicsView, itemTableView, machineWidget)

    itemsListTableView.itemClicked.connect(itemClickHandler)
    
    graphicsView.nodeSelected.connect(nodeSelectioHandler)
    
    machineWidget.calculateClicked.connect(calculateClickHandler)

    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())

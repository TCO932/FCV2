import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QApplication

import FCV2 as fcv2
from data import *
from qtUI.Tabs_ui import Ui_MainWindow
from widgets.Graph import GraphView
from widgets.ItemsListTable import ItemsListTableView
from widgets.ItemTable import ItemTableView
from widgets.MachineWidget import MachineWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    machineWidget = MachineWidget()
    itemTableView = ItemTableView(machineWidget)
    itemsListTableView = ItemsListTableView(RECIPES)

    graphicsView = GraphView(itemTableView)
    ui = Ui_MainWindow(itemsListTableView, graphicsView, itemTableView, machineWidget)
    def itemClickHandler(modelIndex: QModelIndex):
        ui.tabWidget.setCurrentIndex(1)
        itemMeta = ui.itemsListTableView.model().itemsList[modelIndex.row()]
        print(itemMeta)
        speedTree = fcv2.initSpeedTree(itemMeta, 1, ASSENBLING_MACHINE_3)

        graphicsView.build_graph(speedTree)

    
    ui.itemsListTableView.clicked.connect(itemClickHandler)
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())

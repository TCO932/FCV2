import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QApplication

import FCV2 as fcv2
import qtUI.Tabs_ui as tabs
from data import *
from views.Graph import GraphView
from views.ItemsListTable import ItemsListTableView
from views.ItemTable import ItemTableView
from views.MachineTable import MachineTableView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    machineTableView = MachineTableView()
    itemTableView = ItemTableView(machineTableView)
    itemsListTableView = ItemsListTableView(RECIPES)

    graphicsView = GraphView(itemTableView)
    ui = tabs.Ui_MainWindow(itemsListTableView, graphicsView, itemTableView, machineTableView)
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

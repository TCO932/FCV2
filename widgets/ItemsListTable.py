from PyQt6.QtCore import QAbstractTableModel, Qt, pyqtSignal, QModelIndex
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableView

from classes import Item, ItemMeta


class ItemsListTableView(QTableView):
    itemClicked = pyqtSignal(Item)

    def __init__(self, itemsList):
        super().__init__()
        model = ItemMetaListModel(itemsList)
        self.setModel(model)
        self.clicked.connect(self.clickHandler)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().hide()
        # self.setRowHeight(0, 100)
        self.verticalHeader().setDefaultSectionSize(64)

    def clickHandler(self, modelIndex: QModelIndex):
        item: Item = self.model().itemsList[modelIndex.row()]
        self.itemClicked.emit(item)


class ItemMetaListModel(QAbstractTableModel):
    def __init__(self, items: dict[ItemMeta]):
        super().__init__()
        self.itemsList: list[Item] = list(items.values())
        self.fields = ['name']

    def rowCount(self, parent=None):
        return len(self.itemsList)

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return self.itemsList[index.row()].name
        elif role == Qt.ItemDataRole.DecorationRole:
            itemName = self.itemsList[index.row()].name
            pixmap = QPixmap(f'images/{itemName}.png')
            return pixmap
        return None
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QComboBox, QStyledItemDelegate, QTableView

from classes import ItemMeta
from data import ASSENBLING_MACHINES
from widgets.Graph import Node


class ItemTableView(QTableView):
    def __init__(self):
        super().__init__()
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().hide()

    def setItem(self, itemMeta: ItemMeta):
        self.itemMeta = itemMeta
        model = ItemMetaModel(itemMeta)
        self.setModel(model)

class ItemMetaModel(QAbstractTableModel):
    def __init__(self, itemMeta: ItemMeta):
        super().__init__()
        self.itemMeta = itemMeta
        self.fields = [
            'id', 'name', 'speed', 'machineType', 'machinesAmount'
        ]

    def rowCount(self, parent=None):
        return len(self.fields)

    def columnCount(self, parent=None):
        return 1  # Field name and its value

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                field_name = self.fields[index.row()]
                data = getattr(self.itemMeta, field_name)
                return data
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "Value"
            elif orientation == Qt.Orientation.Vertical:
                return self.fields[section]
        return None
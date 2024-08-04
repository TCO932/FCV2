
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QComboBox, QStyledItemDelegate, QTableView

from classes import ItemMeta
from data import ASSENBLING_MACHINES
from widgets.Graph import Node


class ItemTableView(QTableView):
    def __init__(self, machineTableView: QTableView):
        super().__init__()
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().hide()

    def update_info(self, node: Node):
        if node is not None:
            data: ItemMeta = node.itemMeta
            model = ItemMetaModel(data)
            self.setModel(model)
            self.setItemDelegate(ItemMetaDelegate(self.model()))

class ItemMetaModel(QAbstractTableModel):
    def __init__(self, itemMeta: ItemMeta):
        super().__init__()
        self.itemMeta = itemMeta
        self.fields = list(vars(self.itemMeta).keys())
        self.machine_options = list(ASSENBLING_MACHINES.keys())

    def rowCount(self, parent=None):
        return len(self.fields)

    def columnCount(self, parent=None):
        return 1  # Field name and its value

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                field_name = self.fields[index.row()]
                return getattr(self.itemMeta, field_name)
        return None

    def flags(self, index):
        if index.isValid():
            if self.fields[index.row()] == "machine":
                return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.NoItemFlags

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole and index.column() == 0:
            field_name = self.fields[index.row()]
            if field_name == "machine" and value in self.machine_options:
                setattr(self.itemMeta, field_name, value)
                self.dataChanged.emit(index, index)  # Notify that data has changed
                return True
        return False

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "Value"
            elif orientation == Qt.Orientation.Vertical:
                return self.fields[section]  # Return field name
        return None

class ItemMetaDelegate(QStyledItemDelegate):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.machine_options = list(ASSENBLING_MACHINES.keys())  # Predefined values for machine
        self.fields = model.fields

    def createEditor(self, parent, option, index):
        if index.row() == self.fields.index("machine"):
            combo = QComboBox(parent)
            combo.addItems(self.machine_options)
            return combo
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        if index.row() == self.fields.index("machine"):
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        if index.row() == self.fields.index("machine"):
            model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)

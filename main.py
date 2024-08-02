import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QTableView, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPixmapItem, QComboBox, QStyledItemDelegate
from PyQt6.QtCore import Qt, QPoint, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QPainter, QPen, QPixmap
from PyQt6 import QtWidgets
import requests
import FCV2 as fcv2
from classes import ItemMeta, ItemTree
from data import *
import qtUI.Tabs_ui as tabs

class Node(QGraphicsPixmapItem):
    def __init__(self, x, y, itemMeta: ItemMeta, label: str = None, edges=None):
        super().__init__()
        self.itemMeta: ItemMeta = itemMeta

        self.setPixmap(self.load_image(self.itemMeta.image))
        self.setPos(x, y)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable)

        if label is not None:
            self.text_item = QGraphicsTextItem(self)
            self.text_item.setPlainText('{}'.format(label))
            self.text_item.setDefaultTextColor(Qt.GlobalColor.black)
            self.text_item.setPos(x + 10, y + 10)

        self.edges = edges if edges is not None else []

    def load_image(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = QPixmap()
            image.loadFromData(response.content)
            return image
        except Exception as e:
            print(f"Error loading image from {image_url}: {e}")
            return QPixmap()

    def itemChange(self, change, value):
        if change == QGraphicsPixmapItem.GraphicsItemChange.ItemScenePositionHasChanged:
            self.text_item.setPlainText(self.text_item.toPlainText())
            for edge in self.edges:
                edge.update_position()
        if change == QGraphicsPixmapItem.GraphicsItemChange.ItemSelectedChange:
            if value:  # Если узел выбран
                self.scene().views()[0].update_info_panel(self)  # Обновляем информацию в панели
        return super().itemChange(change, value)

class Edge(QGraphicsLineItem):
    def __init__(self, node1, node2):
        super().__init__()
        self.node1 = node1
        self.node2 = node2
        self.setPen(QPen(Qt.GlobalColor.black, 3))
        self.setZValue(-1)
        self.update_position()

    def update_position(self):
        x1 = self.node1.x() + self.node1.pixmap().width() / 2
        y1 = self.node1.y() + self.node1.pixmap().height() / 2
        x2 = self.node2.x() + self.node2.pixmap().width() / 2
        y2 = self.node2.y() + self.node2.pixmap().height() / 2
        self.setLine(x1, y1, x2, y2)

class GraphView(QGraphicsView):
    def __init__(self, itemTableView: QTableView):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.nodes = {}
        self.itemTableView = itemTableView  # Сохраняем ссылку на боковую панель
        self.is_panning = False
        self.last_mouse_position = QPoint()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def add_node(self, x, y, itemMeta: ItemMeta, label: str = None):
        node = Node(x, y, itemMeta, label)
        self.scene().addItem(node)
        self.nodes[node.itemMeta.id] = node
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.scene().addItem(edge)
        node1.edges.append(edge)
        node2.edges.append(edge)

    def build_graph(self, tree: ItemTree):
        self.scene().clear()
        indent: int = 1
        def buildLevel(parentId: str = tree.root, level: int = 1):
            node = tree[parentId]
            nonlocal indent
            x = 100 * indent
            y = 100 * level
            self.add_node(x, y, node, indent)
            children = tree.children(node)
            indent -= 1

            for i, childId in enumerate(children):
                indent += i + 1
                buildLevel(childId, level=level+1)
                self.add_edge(self.nodes[childId], self.nodes[parentId])

        buildLevel()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = True
            self.last_mouse_position = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_panning:
            delta = event.position() - self.last_mouse_position
            self.last_mouse_position = event.position()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - int(delta.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - int(delta.y()))

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoom_factor = 1.2
        if event.angleDelta().y() < 0:
            zoom_factor = 1 / zoom_factor
        view_pos = event.position().toPoint()
        scene_pos = self.mapToScene(view_pos)
        self.centerOn(scene_pos)
        self.scale(zoom_factor, zoom_factor)
        delta = self.mapToScene(view_pos) - self.mapToScene(self.viewport().rect().center())
        self.centerOn(scene_pos - delta)

    def update_info_panel(self, node):
        self.itemTableView.update_info(node)

        
class ItemTableView(QTableView):
    def __init__(self):
        super().__init__()

    def update_info(self, node: Node):
        if node is not None:
            data: ItemMeta = node.itemMeta
            model = ItemMetaModel(data)
            self.setModel(model)
            self.setItemDelegate(ItemMetaDelegate(self.model()))
        else:
            self.label.setText("Select a node to see details")

class ItemMetaModel(QAbstractTableModel):
    def __init__(self, itemMeta: ItemMeta):
        super().__init__()
        self.itemMeta = itemMeta
        self.fields = list(vars(self.itemMeta).keys())
        self.machine_options = list(ASSENBLING_MACHINES.keys())  # Predefined values for machine

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


class ItemsListTableView(QTableView):
    def __init__(self, itemsList):
        super().__init__()
        model = ItemMetaListModel(itemsList)
        self.setModel(model)

    def update_info(self, itemsList: list[ItemMeta]): pass

class ItemMetaListModel(QAbstractTableModel):
    def __init__(self, items: dict[ItemMeta]):
        super().__init__()
        self.itemsList: list[Item] = list(items.values())
        self.fields = ['name']  # Указываем, что у нас есть только одно поле - название предмета

    def rowCount(self, parent=None):
        return len(self.itemsList)

    def columnCount(self, parent=None):
        return 1  # У нас только один столбец для названий предметов

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return self.itemsList[index.row()].name  # Возвращаем название предмета
        # elif role == Qt.ItemDataRole.DecorationRole:
        #     # Предполагаем, что у вас есть ссылка на изображение для заголовка
        #     image_url = self.itemsList[index.row()].image  # Замените на вашу ссылку
        #     pixmap = QPixmap()
        #     pixmap.loadFromData(requests.get(image_url).content)  # Загрузка изображения по URL
        #     return pixmap  # Возвращаем QPixmap для заголовка
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    itemTableView = ItemTableView()
    itemsListTableView = ItemsListTableView(RECIPES)

    graphicsView = GraphView(itemTableView)
    ui = tabs.Ui_MainWindow(graphicsView, itemTableView, itemsListTableView)
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

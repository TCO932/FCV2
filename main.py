import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QTableView, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPixmapItem, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint, QAbstractTableModel
from PyQt6.QtGui import QPainter, QPen, QPixmap
from PyQt6 import QtWidgets
import requests
import treelib as tr
import FCV2 as fcv2
from classes import ItemMeta
from data import *
import qtUI.FCV2_ui as tree
import qtUI.Tabs_ui as tabs

class Node(QGraphicsPixmapItem):
    def __init__(self, x, y, dataNode: tr.Node, label: str = None, edges=None):
        super().__init__()
        self.dataNode: tr.Node = dataNode
        self.data: ItemMeta = dataNode.data

        self.setPixmap(self.load_image(self.data.image))
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
    def __init__(self, info_panel):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.nodes = {}
        self.info_panel = info_panel  # Сохраняем ссылку на боковую панель
        self.is_panning = False
        self.last_mouse_position = QPoint()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def add_node(self, x, y, node: tr.Node, label: str = None):
        node = Node(x, y, node, label)
        self.scene().addItem(node)
        self.nodes[node.dataNode.identifier] = node
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.scene().addItem(edge)
        node1.edges.append(edge)
        node2.edges.append(edge)

    def build_graph(self, tree: tr.Tree):
        indent: int = 1
        def buildLevel(predecessorId: str = tree.root, level: int = 1):
            node: tr.Node = tree[predecessorId]
            nonlocal indent
            x = 100 * indent
            y = 100 * level
            self.add_node(x, y, node, indent)
            children = tree.children(node.identifier)
            indent -= 1

            for i, child in enumerate(children):
                indent += i + 1
                buildLevel(child.identifier, level=level+1)
                self.add_edge(self.nodes[child.identifier], self.nodes[predecessorId])

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
        self.info_panel.update_info(node)

class InfoPanel(QTableView):
    def __init__(self):
        super().__init__()

    def update_info(self, node: Node):
        if (node is not None):
            data: ItemMeta = node.dataNode.data
            model = ItemMetaModel(data)
            self.setModel(model)
        else:
            self.label.setText("Select a node to see details")

class ItemMetaModel(QAbstractTableModel):
    def __init__(self, itemMeta: ItemMeta):
        super().__init__()
        self.itemMeta = itemMeta
        self.fields = list(vars(self.itemMeta).keys())

    def rowCount(self, parent=None):
        return len(self.itemMeta)

    def columnCount(self, parent=None):
        return 1  # Название поля и его значение

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                field_name = self.fields[index.row()]
                return getattr(self.itemMeta, field_name)
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section != 0:
                    return "value" 
            elif orientation == Qt.Orientation.Vertical:
                return self.fields[section]  # Возвращаем название поля
        return None

if __name__ == "__main__":
    # Здесь вы должны инициализировать ваш tree
    craftTree = fcv2.buildCraftTree('utility-science-pack', 1, ASSENBLING_MACHINE_3)
    speedTree = fcv2.buildSpeedTree('utility-science-pack', 1, ASSENBLING_MACHINE_3)


    app = QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    tableView = InfoPanel()

    graphicsView = GraphView(tableView)
    ui = tabs.Ui_MainWindow(graphicsView, tableView)
    ui.setupUi(window)

    graphicsView.build_graph(speedTree)

    window.show()
    sys.exit(app.exec())

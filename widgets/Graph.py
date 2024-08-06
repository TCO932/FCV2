import time

import requests
from PyQt6.QtCore import QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (QGraphicsLineItem, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsTextItem, QGraphicsView,
                             QTableView)

from classes import ItemMeta, ItemTree


class Node(QGraphicsPixmapItem):
    def __init__(self, x, y, itemMeta: ItemMeta, label: str = None, edges=None):
        super().__init__()
        self.itemMeta: ItemMeta = itemMeta

        self.setPixmap(QPixmap(f'images/{itemMeta.name}.png'))
        self.setPos(x, y)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable)

        if label is not None:
            self.text_item = QGraphicsTextItem(self)
            self.text_item.setPlainText('{}'.format(label))
            self.text_item.setDefaultTextColor(Qt.GlobalColor.black)
            self.text_item.setPos(x + 10, y + 10)

        self.edges = edges if edges is not None else []

    def __eq__(self, other):
        return isinstance(other, ItemMeta) and self.itemMeta.id == other.itemMeta.id

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
            if value:
                self.scene().views()[0].nodeSelected.emit(self)
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
    nodeSelected = pyqtSignal(Node)

    def __init__(self, itemTableView: QTableView):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.nodes: dict[str: Node] = {}
        self.itemTableView = itemTableView
        self.is_panning = False
        self.last_mouse_position = QPoint()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def selectNode(self, itemMeta: ItemMeta):
        node: Node | None = self.nodes.get(itemMeta.id)
        if node:
            node.setSelected(True)

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
        self.nodes.clear()
        self.scene().clear()
        indent: int = 1

        def buildLevel(parentId: str = tree.root, level: int = 1):
            node = tree[parentId]
            nonlocal indent
            x = 100 * indent
            y = 100 * level
            self.add_node(x, y, node)
            children = tree.children(node.id)
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
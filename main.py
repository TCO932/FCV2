import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QPixmap
import requests
import treelib as tr
import FCV2 as fcv2
from classes import ItemMeta
from data import *

class Node(QGraphicsPixmapItem):
    def __init__(self, x, y, dataNode: tr.Node, label: str = None, edges=None):
        super().__init__()
        self.dataNode: tr.Node = dataNode
        self.data: ItemMeta = dataNode.data

        self.setPixmap(self.load_image(self.data.item.image))
        self.setPos(x, y)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable)
        # self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable)
        # self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

        if (label is not None):
            # Добавляем текст к узлу
            self.text_item = QGraphicsTextItem(self)
            # self.text_item.setPlainText(self.data.item.name)
            self.text_item.setPlainText('{}'.format(label))
            self.text_item.setDefaultTextColor(Qt.GlobalColor.black)
            self.text_item.setPos(x + 10, y + 10)  # Позиция текста относительно узла

        # Список для хранения линий, связанных с узлом
        self.edges = edges if edges is not None else []

    def load_image(self, image_url):
        """Загружает изображение по URL и возвращает QPixmap."""
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Проверка на ошибки
            image = QPixmap()
            image.loadFromData(response.content)
            return image
        except Exception as e:
            print(f"Error loading image from {image_url}: {e}")
            return QPixmap()  # Возвращаем пустое изображение в случае ошибки

    def itemChange(self, change, value):
        if change == QGraphicsPixmapItem.GraphicsItemChange.ItemScenePositionHasChanged:
            # Обновляем текст при перемещении узла
            self.text_item.setPlainText(self.text_item.toPlainText())
            # Обновляем позиции всех линий, связанных с узлом
            for edge in self.edges:
                edge.update_position()
        if change == QGraphicsPixmapItem.GraphicsItemChange.ItemSelectedChange:
            print('pressed')
            print(self.dataNode)
        return super().itemChange(change, value)

class Edge(QGraphicsLineItem):
    def __init__(self, node1, node2):
        super().__init__()
        self.node1 = node1
        self.node2 = node2
        self.setPen(QPen(Qt.GlobalColor.black, 5))
        self.update_position()

    def update_position(self):
        # Получаем координаты узлов
        x1 = self.node1.x() + self.node1.pixmap().width() / 2
        y1 = self.node1.y() + self.node1.pixmap().height() / 2
        x2 = self.node2.x() + self.node2.pixmap().width() / 2
        y2 = self.node2.y() + self.node2.pixmap().height() / 2
        self.setLine(x1, y1, x2, y2)

class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.nodes = {}  # Словарь для хранения узлов по их id

        self.is_panning = False  # Флаг для отслеживания состояния панорамирования
        self.last_mouse_position = QPoint()  # Хранит последнюю позицию мыши

         # Скрываем полосы прокрутки
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def add_node(self, x, y, node: tr.Node, label: str = None):
        node = Node(x, y, node, label)
        self.scene().addItem(node)
        self.nodes[node.dataNode.identifier] = node  # Сохраняем узел по его id
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.scene().addItem(edge)
        node1.edges.append(edge)  # Добавляем линию в список узла
        node2.edges.append(edge)  # Добавляем линию в список узла

    def build_graph(self, tree: tr.Tree):
        """Строит граф из древовидной структуры."""
        indent: int = 1
        def buildLevel(predecessorId: str = tree.root, level: int = 1):
            node: tr.Node = tree[predecessorId]
            nonlocal indent
            x = 100 * indent   # Примерное распределение по оси X
            y = 100 * level  # Фиксированная позиция по оси Y
            self.add_node(x, y, node)
            children = tree.children(node.identifier)
            indent -= 1

            for i, child in enumerate(children):
                # new_tree = tr.Tree(tree.subtree(tree.root), deep=True)
                indent += i + 1
                buildLevel(child.identifier, level=level+1)
                self.add_edge(self.nodes[child.identifier], self.nodes[predecessorId])

        buildLevel()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = True
            self.last_mouse_position = event.position()  # Сохраняем начальную позицию мыши
            self.setCursor(Qt.CursorShape.ClosedHandCursor)  # Меняем курсор на "рука"

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_panning:
            # Вычисляем смещение
            delta = event.position() - self.last_mouse_position
            self.last_mouse_position = event.position()  # Обновляем последнюю позицию мыши
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - int(delta.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - int(delta.y()))

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)  # Возвращаем курсор в обычное состояние

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = GraphView()
    view.setWindowTitle("Graph from Tree Structure")
    view.resize(800, 600)

    # Здесь вы должны инициализировать ваш tree
    # Например:
    craftTree = fcv2.buildCraftTree('utility-science-pack', 1, ASSENBLING_MACHINE_3)
    # craftTree.show()
    test = []
    view.build_graph(craftTree)

    view.show()
    sys.exit(app.exec())


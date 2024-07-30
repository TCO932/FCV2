import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QPixmap
import requests
import treelib as tr
import FCV2 as fcv2
from data import *

class Node(QGraphicsPixmapItem):
    def __init__(self, x, y, image_url, label="", edges=None):
        super().__init__()
        self.setPixmap(self.load_image(image_url))
        self.setPos(x, y)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

        # Добавляем текст к узлу
        self.text_item = QGraphicsTextItem(self)
        self.text_item.setPlainText(label)
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

    def add_node(self, x, y, id, image_url):
        node = Node(x, y, image_url=image_url)
        self.scene().addItem(node)
        self.nodes[id] = node  # Сохраняем узел по его id
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.scene().addItem(edge)
        node1.edges.append(edge)  # Добавляем линию в список узла
        node2.edges.append(edge)  # Добавляем линию в список узла

    def build_graph(self, tree: tr.Tree):
        """Строит граф из древовидной структуры."""
        for i, (key, node) in enumerate(tree.nodes.items()):
            node_id = key
            parent_id = node.bpointer
            # Определяем позицию узла
            x = 100 * (i + 1)  # Примерное распределение по оси X
            y = 100  # Фиксированная позиция по оси Y
            self.add_node(x, y, id=node_id, image_url=node.data.item.image)

            # Если у узла есть родитель, добавляем ребро
            if parent_id is not None:
                parent_node = self.nodes.get(parent_id)
                if parent_node:
                    self.add_edge(self.nodes[node_id], parent_node)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = GraphView()
    view.setWindowTitle("Graph from Tree Structure")
    view.resize(800, 600)

    # Здесь вы должны инициализировать ваш tree
    # Например:
    craftTree = fcv2.buildCraftTree('rocket-part', 100, ASSENBLING_MACHINE_3)
    craftTree.show()
    view.build_graph(craftTree)

    view.show()
    sys.exit(app.exec())


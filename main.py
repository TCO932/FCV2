import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QMouseEvent

class Node(QGraphicsEllipseItem):
    def __init__(self, x, y, radius=20):
        super().__init__(x, y, radius, radius)
        self.setBrush(Qt.GlobalColor.blue)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsScenePositionChanges)

        # Добавляем текст к узлу
        self.text_item = QGraphicsTextItem(self)
        self.text_item.setPlainText(f"({x}, {y})")
        self.text_item.setDefaultTextColor(Qt.GlobalColor.white)
        self.text_item.setPos(x + radius / 4, y + radius / 4)

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemScenePositionHasChanged:
            # Обновляем текст при перемещении узла
            self.text_item.setPlainText(f"({value.x():.1f}, {value.y():.1f})")
        return super().itemChange(change, value)

class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Добавляем узлы
        self.add_node(50, 50)
        self.add_node(150, 150)
        self.add_node(250, 50)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Устанавливаем режим перетаскивания

    def add_node(self, x, y):
        node = Node(x, y)
        self.scene().addItem(node)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Включаем режим перетаскивания
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)  # Отключаем режим перетаскивания
        super().mouseReleaseEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = GraphView()
    view.setWindowTitle("Interactive Graph Nodes with Panning")
    view.resize(400, 300)
    view.show()
    sys.exit(app.exec())

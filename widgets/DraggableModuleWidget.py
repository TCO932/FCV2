from classes import Module
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt6.QtGui import QPixmap, QDrag
from PyQt6.QtCore import Qt, QMimeData


class DraggableModule(QLabel):
    def __init__(self, module: Module):
        super().__init__()
        self.module = module
        pixmap = QPixmap(f'images/{module.name}.png')
        self.setPixmap(pixmap)
        self.setFixedSize(32, 32)
        self.setStyleSheet("border: 4px outset gray;")
        self.setScaledContents(True)
        self.setAcceptDrops(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setImageData(self.pixmap().toImage())
            mime_data.setText(self.module.toJSON())
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)

class ModuleDropSlot(QFrame):
    def __init__(self, module: Module = None):
        super().__init__()
        self.module = module
        self.setFixedSize(32, 32)
        self.setStyleSheet("border: 4px inset gray;")
        self.setAcceptDrops(True)

        if module:
            pixmap = QPixmap(f'images/{module.name}.png')
            self.setPixmap(pixmap)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage() and event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasImage() and event.mimeData().hasText():
            image = event.mimeData().imageData()
            pixmap = QPixmap.fromImage(image)
            self.setPixmap(pixmap)

            text = event.mimeData().text()
            self.module = Module.fromJSON(text)
            print(self.module)

            event.acceptProposedAction()

    def setData(self, module: Module):
        pixmap = QPixmap(f'images/{module.name}.png')
        self.setPixmap(pixmap)

        self.module = module

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.module = None
            self.clear()

    def clear(self):
        self.pixmap = None
        self.clear()  # Clear the QLabel
        self.setStyleSheet("border: 4px inset gray;")


    def setPixmap(self, pixmap):
        self.clear()
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setFixedSize(32, 32)
        label.setScaledContents(True)
        label.move(0, 0)
        label.show()

    def clear(self):
        for child in self.findChildren(QLabel):
            child.deleteLater()




if __name__ == "__main__":
    class DragDropApp(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Drag and Drop Images")
            self.setGeometry(100, 100, 400, 300)

            layout = QVBoxLayout()

            # Создаем изображения для перетаскивания
            self.image_labels = []
            for module in MODULES.values():
                draggableModule = DraggableModule(module)
                self.image_labels.append(draggableModule)
                layout.addWidget(draggableModule)

            # Создаем слоты для перетаскивания
            slot_layout = QHBoxLayout()
            for _ in range(4):  # Количество слотов
                slot = ModuleDropSlot()
                slot_layout.addWidget(slot)

            layout.addLayout(slot_layout)
            self.setLayout(layout)

    PRODUCTIVITY_MODULE_1 = Module('productivity-module', 0.04, -0.05)
    PRODUCTIVITY_MODULE_2 = Module('productivity-module-2', 0.06, -0.1)
    PRODUCTIVITY_MODULE_3 = Module('productivity-module-3', 0.1, -0.15)

    SPEED_MODULE_1 = Module('speed-module', 0.0, 0.2)
    SPEED_MODULE_2 = Module('speed-module-2', 0.0, 0.3)
    SPEED_MODULE_3 = Module('speed-module-3', 0.0, 0.5)

    MODULES = {
        'productivity-module': PRODUCTIVITY_MODULE_1,
        'productivity-module-2': PRODUCTIVITY_MODULE_2,
        'productivity-module-3': PRODUCTIVITY_MODULE_3,
        'speed-module': SPEED_MODULE_1,
        'speed-module-2': SPEED_MODULE_2,
        'speed-module-3': SPEED_MODULE_3,
    }

    app = QApplication(sys.argv)
    window = DragDropApp()
    window.show()
    sys.exit(app.exec())
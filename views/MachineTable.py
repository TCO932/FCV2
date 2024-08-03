import requests
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (QGraphicsLineItem, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsTextItem, QGraphicsView,
                             QTableView)

from classes import ItemMeta, ItemTree

class MachineTableView(QTableView):
    pass
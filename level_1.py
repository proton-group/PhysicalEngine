#level 1
from Engine import physics
import sys
from PySide6.QtCore import Qt, QRect, QEvent
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QIcon, QImage, QFont
class level(QMainWindow):
    def __init__(self,app, width):
        super().__init__()
        self.setWindowTitle("Level1")
        self.width = width
        self.pos = []
        self.archive = []
        self.num = 0
        self.pause = True
        self.p = physics()

    def buttonsl(self):
        exbut = QPushButton("<-", self)

        exbut.setStyleSheet("background-color: blue")
        exbut.setFixedSize(100, 50)
        exbut.move(100, 0)
        exbut.clicked.connect(self.closeit)

    def paintEvent(self, event):
        #try:
        qp = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        self.painter(qp)
        #except:
            #self.update()

    def painter(self, qp):
        lastx, lasty = self.pos[0][0], self.pos[0][1]
        for point in self.pos:
            qp.drawLine(lastx, lasty, point[0], point[1])
            lastx, lasty = point[0], point[1]
        for pos in self.archive:
            pos = self.p.gravity(pos)
            if pos != []:
                lastx, lasty = pos[0][0], pos[0][1]
                for point in pos:
                    qp.drawLine(lastx, lasty, point[0], point[1])
                    lastx, lasty = point[0], point[1]

    def mouseMoveEvent(self, event):
        self.pos.append((event.x(), event.y()))
        self.update()

    def mousePressEvent(self, event):
        self.archive.append(self.pos)
        self.pos = []

    def closeit(self):
        self.close()
        


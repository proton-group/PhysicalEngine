import sys
from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QIcon, QImage, QFont
from level_1 import level

class Window(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("test")
        screen = app.primaryScreen()
        self.size = screen.size()
        self.buttons()
        self.showFullScreen()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.painter(qp)
        qp.end()

    def painter(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        font = QFont("Times", 60, QFont.Bold)
        qp.setFont(font)

        qp.drawText(self.size.height()/1.35, self.size.width()/10, 500, 200, 0, "Bridges")
        
    def Picture(self):
        pass

    def level_1(self):
        self.win = level(app, self.size.width())
        self.win.showFullScreen()
        self.win.buttonsl()

    def buttons(self):
        exbut = QPushButton("X", self)
        lvl1_but = QPushButton(self)

        #lvl1_but.setIcon(QIcon("lvl1.png"))
        lvl1_but.setText("Level 1")
        lvl1_but.setFont(QFont("Times", 20, QFont.Bold))
        lvl1_but.setFixedSize(100, 100)
        lvl1_but.move(self.size.height()/2, self.size.width()/5)
        lvl1_but.clicked.connect(self.level_1)

        exbut.setStyleSheet("background-color: red")
        exbut.setFixedSize(50, 50)
        exbut.move(self.size.width()-50, 0)
        exbut.clicked.connect(self.exit)

    def exit(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)


    win = Window(app)
    sys.exit(app.exec_())


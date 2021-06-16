#level 1
from Engine import physics, body
import sys
import ast
from PySide6.QtCore import Qt, QRect, QEvent, QTimer
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QIcon, QImage, QFont
#rober serjic algoritms curs

class level(QMainWindow):
    def __init__(self, app, width):
        super().__init__()
        self.check = True
        self.setWindowTitle("Level1")
        self.width = width
        self.pos = []
        self.archive = []
        self.num = 0
        self.pause = True
        self.p = physics()
        self.closebuttons()
        self.backplan = self.loadstate("backplan.txt")
        carpos = self.loadstate("car.txt") #тапл из двух или трех массивов 
        self.wheels = []
        self.carbody = []
        for pos in carpos[:2]:
            wheel = body()
            wheel.pos = pos
            self.wheels.append(wheel)
        carbody = body()
        carbody.pos = carpos[0]
        self.car = [carbody]
        self.time = QTimer(self)
        self.time.start(1)
        self.time.timeout.connect(self.timer)
        self.update()

    def closebuttons(self):
        self.closebut = QPushButton("<-", self)

        self.closebut.setStyleSheet("background-color: yellow")
        self.closebut.setFixedSize(100, 50)
        self.closebut.move(self.width - 100, 0)
        self.closebut.clicked.connect(self.closeit)

    def paintEvent(self, event):
        #try:
        qp = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        self.painter(qp)
        #except:
            #self.update()
            #pass
            
    def hexpaint(self, qp, pos):
        if pos != []:
            lastx, lasty = pos[0][0], pos[0][1]
            for point in pos:
                qp.drawLine(lastx, lasty, point[0], point[1])
                lastx, lasty = point[0], point[1]
    
    def painter(self, qp): # В класс и разбить на функции
        self.hexpaint(qp, self.pos)
    
        for pos in self.backplan:
            self.hexpaint(qp, pos)
        
        self.p.check_collision(self.wheels, self.archive, self.backplan)
        self.p.check_collision(self.carbody, self.wheels, self.backplan)
        for obj in self.wheels:
            if obj.pcollision:
                obj = self.p.moution(obj, "up") #сделать, только если проп с колесами, чтобы не обрабытывть фронт удары
                obj.pcollision = False
            else:
                obj = self.p.moution(obj, "right")
            self.hexpaint(qp, obj.pos)
        #print(self.p.rotation_objects)
        self.p.check_collision(self.archive, self.archive, self.backplan)

        #self.p.check_collision(self.carid, self.archive, self.backplan)
        for obj in self.archive:
            self.p.rotation(self.p.rot_direction_chooser(obj), obj)
            self.hexpaint(qp, obj.pos)

    def mouseMoveEvent(self, event):
        self.pos.append((event.x(), event.y()))
        #self.update()

    def mouseReleaseEvent(self, event):
        new_body = body()
        if self.pos != []:
            new_body.pos = self.pos
            self.archive.append(new_body)
            self.pos = []
        self.update()
        
    def closeit(self):
        self.close()

    def savestate(self):
        f = open("data.txt", "w")
        f.write(",".join(map(str, self.archive)) + "\n")
        f.close()

    def loadstate(self, file):
        f = open(file, "r")
        return ast.literal_eval(f.read())
        
    def timer(self):
        self.update()
        self.time.start(1) #в теории каждый 10 миллисекунд достаточно, чтобы пользователь не заметил пропуски коллизий



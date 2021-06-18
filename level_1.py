#level 1
from Engine import physics, body
import sys
import ast
from PySide6.QtCore import Qt, QRect, QEvent, QTimer
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QIcon, QImage, QFont
#rober serjic algoritms curs
class Node:
    def __init__(self):
        self.memory = None
        self.data = None
class fifo:
    def __init__(self):
        self.base = Node()
        self.len = 0
        self.fifoblock = False

    def add(self, data):
        self._add(data, self.base)

    def _add(self, data, node):
        if self.base.data == None:
            self.base.data = data
        else:
            if node.memory != None:
                self._add(data, node.memory)
            else:
                node.memory = Node()
                self.len += 1
                node.memory.data = data
    def read(self):
        data = self.base.data
        if not self.fifoblock:
            self.add(data)
        if self.base.memory != None:
            self.base = self.base.memory
            self.len -= 1
        else:
            self.base = Node()
        return data

    def control(self, instruction):
        if instruction == "break":
            self.fifoblock = True
        if instruction == "lock":
            self.fifoblock = False
    def clear(self):
        self.base = Node()



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
        self.startbutton()
        view = body()
        view.pos = self.loadstate("backplan2.txt")
        self.backplan = [view]
        self.car = []
        car = body()
        car.pos = self.loadstate("car.txt") #тапл из двух или трех массивов 
        self.car.append(car)
        self.time = QTimer(self)
        self.time.start(100)
        self.time.timeout.connect(self.timer)
        self.paintfq = QTimer(self)
        self.paintfq.start(1)
        self.paintfq.timeout.connect(self.fq)
        self.timeblock = True
        self.paint_buffer = fifo()
        self.update()

    def closebuttons(self):
        self.closebut = QPushButton("<-", self)

        self.closebut.setStyleSheet("background-color: yellow")
        self.closebut.setFixedSize(100, 50)
        self.closebut.move(self.width - 100, 0)
        self.closebut.clicked.connect(self.closeit)
    
    def startbutton(self):
        self.startbut = QPushButton("START", self)
        self.startbut.setStyleSheet("background-color: red")
        self.startbut.setFixedSize(100, 100)
        self.startbut.move(self.width - 100, 500)
        self.startbut.clicked.connect(self.start)

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
        if pos != [] and pos != None:
            lastx, lasty = pos[0][0], pos[0][1]
            for point in pos:
                qp.drawLine(lastx, lasty, point[0], point[1])
                lastx, lasty = point[0], point[1]
    
    def painter(self, qp): # В класс и разбить на функции
        self.hexpaint(qp, self.pos)       
        for i in range(self.paint_buffer.len):
            self.hexpaint(qp, self.paint_buffer.read())

    def mouseMoveEvent(self, event):
        self.pos.append((event.x(), event.y()))
        #self.update()

    def mouseReleaseEvent(self, event):
        new_body = body()
        if self.pos != []:
            new_body.pos = self.pos
            self.archive.append(new_body)
            self.pos = []
        #self.update()
        
    def closeit(self):
        self.close()

    def savestate(self):
        f = open("backplan2.txt", "w")
        f.write(",".join(map(str, self.archive)) + "\n")
        f.close()

    def loadstate(self, file):
        f = open(file, "r")
        return ast.literal_eval(f.read())
    
    def start(self):
        self.timeblock = False

    def fq(self):
        self.paintfq.start(1000)
        #self.repaint()

    def timer(self):
        self.paint_buffer.clear()
        #self.timeblock = not self.timeblock
        self.paint_buffer.add(self.pos)
    
        for obj in self.backplan:
            #self.hexpaint(qp, obj.pos)
            self.paint_buffer.add(obj.pos)
        
        if self.timeblock == False:
            self.p.check_collision(self.car, self.archive)
            self.p.check_collision(self.car, self.backplan)
            for obj in self.car:
                if obj.pcollision:
                    obj = self.p.moution(obj, "up") #сделать, только если проп с колесами, чтобы не обрабытывть фронт удары
                    obj.pcollision = False
                else:
                    obj = self.p.moution(obj, "right")
                #self.hexpaint(qp, obj.pos)
                self.paint_buffer.add(obj.pos)
        
        
        #self.hexpaint(qp, self.car[0].pos)
        #print(self.p.rotation_objects)
        
        self.p.check_collision(self.archive, self.archive)
        self.p.check_collision(self.archive, self.backplan)

        #self.p.check_collision(self.carid, self.archive, self.backplan)
        for obj in self.archive:
            #self.hexpaint(qp, obj.pos)
            if obj.pos != []:
                self.paint_buffer.add(obj.pos)
        self.repaint()
        self.time.start(10) #в теории каждый 10 миллисекунд достаточно, чтобы пользователь не заметил пропуски коллизий




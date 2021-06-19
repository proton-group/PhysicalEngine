#level 1
from Engine import physics, body
import sys
import ast
from fifo import fifo
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
        self.paint_buffer = []
        self.check = False
        self.win = self.loadstate("wintext.txt")
        self.winlist = []
        for pos in self.win:
            winobj = body()
            winobj.pos = pos
            self.winlist.append(winobj)
        self.wincheck = False

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
        for i in range(len(self.paint_buffer)):
            self.hexpaint(qp, self.paint_buffer[i])

    def mouseMoveEvent(self, event):
        self.pos.append((event.x(), event.y()))
        #self.update()

    def mouseReleaseEvent(self, event):
        new_body = body()
        if self.pos != []:
            new_body.pos = self.pos
            self.archive.append(new_body)
            #self.archive.append(self.pos)
            #self.savestate()
            self.pos = []
        #self.update()
        
    def closeit(self):
        self.close()

    def savestate(self):
        f = open("backplan3.txt", "w")
        f.write(",".join(map(str, self.archive)) + "\n")
        f.close()

    def loadstate(self, file):
        f = open(file, "r")
        return ast.literal_eval(f.read())
    
    def start(self):
        self.timeblock = False

    def fq(self):
        self.paintfq.start(50)
        for id_a, id_b in self.p.idpoint(self.archive, self.archive):
            self.p.prop_check(id_a, id_b)
        self.repaint()

    def timer(self):
        
        self.paint_buffer.clear()
        if self.timeblock == True:
            #self.timeblock = not self.timeblock
            self.paint_buffer.append(self.pos)
            
        for obj in self.backplan:
            #self.hexpaint(qp, obj.pos)
            self.paint_buffer.append(obj.pos)
            
        if self.timeblock == False:
            self.p.check_collision(self.car, self.archive)
            self.p.check_collision(self.car, self.backplan)
            
            for obj in self.car:
                if obj.pcollision:
                    self.check = True
                    obj = self.p.moution(obj, "up") #сделать, только если проп с колесами, чтобы не обрабытывть фронт удары
                    obj.pcollision = False
                elif self.check:
                    obj = self.p.moution(obj, "right")
                #self.hexpaint(qp, obj.pos)
                self.paint_buffer.append(obj.pos)
        
        
        #self.hexpaint(qp, self.car[0].pos)
        #print(self.p.rotation_objects)

        if self.timeblock == True:
            self.p.check_collision(self.archive, self.archive)
            self.p.check_collision(self.archive, self.backplan)

        #self.p.check_collision(self.carid, self.archive, self.backplan)
        for obj in self.archive:
            #self.hexpaint(qp, obj.pos)
            if obj.pos != []:
                self.paint_buffer.append(obj.pos)
        if self.wincheck == True:
            for obj in self.winlist:
                self.paint_buffer.append(obj.pos)
        self.winzone(self.car)
        #self.repaint()
        self.time.start(10) #в теории каждый 10 миллисекунд достаточно, чтобы пользователь не заметил пропуски коллизий
    
    def winzone(self, car):
        zone = [800, 1500, 0, 2000]
        if self.p.minmax(car[0].pos)[0] > 1600:
            self.timeblock = True
            self.wincheck = True





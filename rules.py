from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys


class rules(QWidget):
    def __init__(self):  
        super().__init__()
        self.ui()
    
    def ui(self):
        box = QVBoxLayout()
        rule = QLabel("Вы - мостостроитель, ваша задача: помочь автомобилисту справиться с дорожными препятствиями. Наведите курсор мыши в нужное место, чтобы нарисовать дорожный объект, зажмите ЛКМ и проведите линию. Объект упадет под действием гравитации. Справа на уровне находится кнопка START для запуска машинки.")
        rule.setWordWrap(True)
        rule.setFont(QFont("Times", 20, QFont.Bold))
        rule.setAlignment(Qt.AlignCenter)
        box.addWidget(rule)
        self.setLayout(box)
        self.setFixedSize(640, 480)
        self.setWindowTitle("Rules")
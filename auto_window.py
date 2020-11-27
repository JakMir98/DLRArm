from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton


class AutoWindow(QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = "Auto mode"
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 380
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.switch_btn = QPushButton('&+', self)
        self.switch_btn.setToolTip('Dodawanie')
        self.switch_btn.clicked.connect(self.switch)

    def switch(self):
        self.switch_window.emit()
        self.close()

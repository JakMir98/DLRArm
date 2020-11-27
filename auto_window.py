from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton


class AutoWindow(QWidget):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = "Auto mode"
        self.left = 900
        self.top = 500  # 70
        self.width = 800
        self.height = 410
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.switch_btn = QPushButton('manual', self)
        self.switch_btn.setToolTip('Przełącz na tryb manualny.')
        self.switch_btn.clicked.connect(self.switch)

    def switch(self):
        self.switch_window.emit()
        self.close()

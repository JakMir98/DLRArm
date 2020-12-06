from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton


class AutoWindow(QWidget):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = "Auto mode"
        self.left = 900
        self.top = 500  # 70
        self.width = 800
        self.height = 410
        self.angle = [90, 90, 90, 90, 90, 90]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.start_btn = QPushButton('ułóż zdanie', self)
        self.start_btn.setToolTip('Rozpocznij układanie słowa.')
        self.start_btn.setGeometry(4, 305, 145, 100)
        self.start_btn.clicked.connect(self.switch)

        self.switch_btn = QPushButton('tryb manualny', self)
        self.switch_btn.setToolTip('Przełącz na tryb manualny.')
        self.switch_btn.setGeometry(153, 305, 145, 100)
        self.switch_btn.clicked.connect(self.switch)

        self.instructions_btn = QPushButton('instrukcja', self)
        self.instructions_btn.setToolTip('Wyświetl instrukcję obsługi ramienia.')
        self.instructions_btn.setGeometry(302, 305, 145, 100)
        self.instructions_btn.clicked.connect(self.switch)

        self.settings_btn = QPushButton('ustawienia', self)
        self.settings_btn.setToolTip('Zmień ustawienia programu.')
        self.settings_btn.setGeometry(451, 305, 145, 100)
        self.settings_btn.clicked.connect(self.switch)

        self.label_logs = QLabel(self)
        self.label_logs.setText('logs')
        self.label_logs.setAlignment(Qt.AlignTop)
        self.label_logs.setStyleSheet("QLabel {background-color: lightgrey;}")
        self.label_logs.setGeometry(600, 0, 200, 410)

    def serial_write(self):
        arduino.write(chr(200))
        arduino.write(chr(self.angle[0]))
        arduino.write(chr(self.angle[1]))
        arduino.write(chr(self.angle[2]))
        arduino.write(chr(self.angle[3]))
        arduino.write(chr(self.angle[4]))
        arduino.write(chr(self.angle[5]))

    def switch(self):
        self.switch_window.emit()
        self.close()

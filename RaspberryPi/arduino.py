import serial
import pytesseract
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QPushButton, QDialog, QVBoxLayout

global arduino
arduino = serial.Serial("COM13", 9600)  # "/dev/ttyXX" for Linux
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\pawel\\Desktop\\tess\\tesseract.exe'


class InformationDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InformationDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Information window")
        # here goes text to information window
        self.text = QLabel("TEST", self)

        self.button = QPushButton('OK', self)
        self.button.clicked.connect(self.close)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    @pyqtSlot()
    def close(self):
        self.accept()

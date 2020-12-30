from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLineEdit, QSlider
import numpy as np
from arduino import *


class ManualWindow(QWidget):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = "Manual mode"
        self.left = 900
        self.top = 500
        self.width = 800
        self.height = 410
        self.angle = [90, 90, 90, 90, 90, 90]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.center_btn = QPushButton('pozycja neutralna', self)
        self.center_btn.setToolTip('Ustaw ramię w pozycji neutralnej.')
        self.center_btn.setGeometry(595, 5, 200, 100)
        self.center_btn.clicked.connect(self.switch)

        self.switch_btn = QPushButton('tryb automatyczny', self)
        self.switch_btn.setToolTip('Przełącz na tryb automatyczny.')
        self.switch_btn.setGeometry(595, 105, 200, 100)
        self.switch_btn.clicked.connect(self.switch)

        self.instructions_btn = QPushButton('instrukcja', self)
        self.instructions_btn.setToolTip('Wyświetl instrukcję obsługi ramienia.')
        self.instructions_btn.setGeometry(595, 205, 200, 100)
        self.instructions_btn.clicked.connect(self.instructions)

        self.slider_pwm1 = QSlider(Qt.Vertical, self)
        self.slider_pwm1.setGeometry(30, 50, 50, 300)
        self.slider_pwm1.setValue(90)
        self.slider_pwm1.setMaximum(180)
        self.slider_pwm1.valueChanged[int].connect(self.pwm1)
        self.text_pwm1 = QLineEdit(self)
        self.text_pwm1.setGeometry(25, 360, 50, 25)
        self.text_pwm1.setText('90')
        self.text_pwm1.setReadOnly(True)
        self.label_pwm1 = QLabel(self)
        self.label_pwm1.setText('servo 1')
        self.label_pwm1.setGeometry(30, 15, 50, 20)

        self.slider_pwm2 = QSlider(Qt.Vertical, self)
        self.slider_pwm2.setGeometry(120, 50, 50, 300)
        self.slider_pwm2.setValue(90)
        self.slider_pwm2.setMaximum(180)
        self.slider_pwm2.valueChanged[int].connect(self.pwm2)
        self.text_pwm2 = QLineEdit(self)
        self.text_pwm2.setGeometry(115, 360, 50, 25)
        self.text_pwm2.setText('90')
        self.text_pwm2.setReadOnly(True)
        self.label_pwm2 = QLabel(self)
        self.label_pwm2.setText('servo 2')
        self.label_pwm2.setGeometry(120, 15, 50, 20)

        self.slider_pwm3 = QSlider(Qt.Vertical, self)
        self.slider_pwm3.setGeometry(210, 50, 50, 300)
        self.slider_pwm3.setValue(90)
        self.slider_pwm3.setMaximum(180)
        self.slider_pwm3.valueChanged[int].connect(self.pwm3)
        self.text_pwm3 = QLineEdit(self)
        self.text_pwm3.setGeometry(205, 360, 50, 25)
        self.text_pwm3.setText('90')
        self.text_pwm3.setReadOnly(True)
        self.label_pwm3 = QLabel(self)
        self.label_pwm3.setText('servo 3')
        self.label_pwm3.setGeometry(210, 15, 50, 20)

        self.slider_pwm4 = QSlider(Qt.Vertical, self)
        self.slider_pwm4.setGeometry(300, 50, 50, 300)
        self.slider_pwm4.setValue(90)
        self.slider_pwm4.setMaximum(180)
        self.slider_pwm4.valueChanged[int].connect(self.pwm4)
        self.text_pwm4 = QLineEdit(self)
        self.text_pwm4.setGeometry(295, 360, 50, 25)
        self.text_pwm4.setText('90')
        self.text_pwm4.setReadOnly(True)
        self.label_pwm4 = QLabel(self)
        self.label_pwm4.setText('servo 4')
        self.label_pwm4.setGeometry(300, 15, 50, 20)

        self.slider_pwm5 = QSlider(Qt.Vertical, self)
        self.slider_pwm5.setGeometry(390, 50, 50, 300)
        self.slider_pwm5.setValue(90)
        self.slider_pwm5.setMaximum(180)
        self.slider_pwm5.valueChanged[int].connect(self.pwm5)
        self.text_pwm5 = QLineEdit(self)
        self.text_pwm5.setGeometry(385, 360, 50, 25)
        self.text_pwm5.setText('90')
        self.text_pwm5.setReadOnly(True)
        self.label_pwm5 = QLabel(self)
        self.label_pwm5.setText('servo 5')
        self.label_pwm5.setGeometry(390, 15, 50, 20)

        self.slider_pwm6 = QSlider(Qt.Vertical, self)
        self.slider_pwm6.setGeometry(480, 50, 50, 300)
        self.slider_pwm6.setValue(90)
        self.slider_pwm6.setMaximum(180)
        self.slider_pwm6.valueChanged[int].connect(self.pwm6)
        self.text_pwm6 = QLineEdit(self)
        self.text_pwm6.setGeometry(475, 360, 50, 25)
        self.text_pwm6.setText('90')
        self.text_pwm6.setReadOnly(True)
        self.label_pwm6 = QLabel(self)
        self.label_pwm6.setText('servo 6')
        self.label_pwm6.setGeometry(480, 15, 50, 20)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.serial_write)
        self.timer.start()

    def pwm1(self, value):
        self.text_pwm1.setText(str(value))
        self.angle[0] = value

    def pwm2(self, value):
        self.text_pwm2.setText(str(value))
        self.angle[1] = value

    def pwm3(self, value):
        self.text_pwm3.setText(str(value))
        self.angle[2] = value

    def pwm4(self, value):
        self.text_pwm4.setText(str(value))
        self.angle[3] = value

    def pwm5(self, value):
        self.text_pwm5.setText(str(value))
        self.angle[4] = value

    def pwm6(self, value):
        self.text_pwm6.setText(str(value))
        self.angle[5] = value

    def instructions(self):
        dlg = InformationDialog(self)
        dlg.text.setText(
            "Here goes our long text\n of course it can be multiline")
        dlg.exec_()

    def serial_write(self):
        arduino.write([np.uint8(200), np.uint8(self.angle[0]), np.uint8(self.angle[1]), np.uint8(self.angle[2]),
                                           np.uint8(self.angle[3]), np.uint8(self.angle[4]), np.uint8(self.angle[5])])
        print([np.uint8(200), np.uint8(self.angle[0]), np.uint8(self.angle[1]), np.uint8(self.angle[2]),
                                           np.uint8(self.angle[3]), np.uint8(self.angle[4]), np.uint8(self.angle[5])])

    def switch(self):
        self.timer.stop()
        self.switch_window.emit()
        self.close()


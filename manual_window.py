from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QSlider


class ManualWindow(QWidget):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = "Manual mode"
        self.left = 900
        self.top = 500
        self.width = 800
        self.height = 410
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.switch_btn = QPushButton('auto', self)
        self.switch_btn.setToolTip('Przełącz na tryb automatyczny.')
        self.switch_btn.setGeometry(595, 5, 200, 100)
        self.switch_btn.clicked.connect(self.switch)

        self.switch_btn = QPushButton('auto', self)
        self.switch_btn.setToolTip('Przełącz na tryb automatyczny.')
        self.switch_btn.setGeometry(595, 105, 200, 100)
        self.switch_btn.clicked.connect(self.switch)

        self.switch_btn = QPushButton('auto', self)
        self.switch_btn.setToolTip('Przełącz na tryb automatyczny.')
        self.switch_btn.setGeometry(595, 205, 200, 100)
        self.switch_btn.clicked.connect(self.switch)

        self.switch_btn = QPushButton('auto', self)
        self.switch_btn.setToolTip('Przełącz na tryb automatyczny.')
        self.switch_btn.setGeometry(595, 305, 200, 100)
        self.switch_btn.clicked.connect(self.switch)

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

    def pwm1(self, value):
        self.text_pwm1.setText(str(value))

    def pwm2(self, value):
        self.text_pwm2.setText(str(value))

    def pwm3(self, value):
        self.text_pwm3.setText(str(value))

    def pwm4(self, value):
        self.text_pwm4.setText(str(value))

    def pwm5(self, value):
        self.text_pwm5.setText(str(value))

    def pwm6(self, value):
        self.text_pwm6.setText(str(value))

    def switch(self):
        self.switch_window.emit()
        self.close()

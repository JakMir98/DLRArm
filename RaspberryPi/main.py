from PyQt5 import QtWidgets
import cv2
import sys
import auto_window
import manual_window


class Controller:

    def __init__(self):
        pass

    def show_manual(self):
        self.manual = manual_window.ManualWindow()
        self.manual.switch_window.connect(self.show_auto)
        self.manual.show()

    def show_auto(self):
        self.auto = auto_window.AutoWindow()
        self.auto.switch_window.connect(self.show_manual)
        self.auto.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_manual()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

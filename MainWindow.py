import time
from PyQt5.QtWidgets import QWidget
from Connection import Connection


class MainWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self, None)
        self.resize(800, 600)

        self.c = Connection(self.updateInfo)
        self.c.start()

        self.setupUI()

    def setupUI(self):
        self.resize(800, 600)
        self.setWindowTitle('MuDepression')
        self.show()
        self.updateInfo(0, False)

    def updateInfo(self, freq, val):
        if val:
            self.setStyleSheet("background-color: green;")
        else:
            self.setStyleSheet("background-color: red;")
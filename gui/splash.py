import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class Window1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 1")
        # ... Add widgets to Window1

class Window2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 2")
        # ... Add widgets to Window2
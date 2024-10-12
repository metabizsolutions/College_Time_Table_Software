import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class UpdateDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Data")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Update Data Here")
        self.label.setFont(QFont("Georgia", 24, QFont.Bold))
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

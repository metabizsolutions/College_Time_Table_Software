import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CreateTimetableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Timetable")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)
        
        # You can add widgets for creating the timetable here
        self.label = QLabel("Create Timetable Here")
        self.label.setFont(QFont("Georgia", 24, QFont.Bold))
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

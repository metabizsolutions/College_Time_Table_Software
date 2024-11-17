from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class WorkloadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workload Management")
        self.setGeometry(300, 200, 600, 400)

        # Set layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add existing buttons (example)
        self.manage_workload_button = QPushButton("Manage Workload")
        self.manage_workload_button.setStyleSheet(self.get_button_style())
        self.layout.addWidget(self.manage_workload_button)

        # Add the new button
        self.workload_analysis_button = QPushButton("Workload Analysis")
        self.workload_analysis_button.setStyleSheet(self.get_button_style())
        self.workload_analysis_button.clicked.connect(self.open_workload_analysis)
        self.layout.addWidget(self.workload_analysis_button)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #181818;
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                width: 300px;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border: 2px solid #ffffff;
            }
        """

    def open_workload_analysis(self):
        # Define what happens when the new button is clicked
        print("Opening Workload Analysis Window!")

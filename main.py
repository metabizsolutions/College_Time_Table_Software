import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import database  # Assuming this is your database.py file with the create_database function

class TimetableCreationWindow(QWidget):
    def __init__(self, db_name):
        super().__init__()
        self.setWindowTitle("Create Timetable")
        self.setGeometry(100, 100, 1280, 720)

        layout = QVBoxLayout(self)

        # Header label
        label = QLabel("Create Timetable")
        label.setFont(QFont("Arial", 24, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Additional UI components can be added here for timetable creation
        self.setLayout(layout)


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window size to 1280x720
        self.setWindowTitle("Timetable Management System")
        self.setGeometry(100, 100, 1280, 720)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add logo in the center
        self.add_logo()

        # Styling the window and buttons
        self.init_ui()

    def add_logo(self):
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")  # Load the logo image
        logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio))  # Scale the logo
        logo_label.setAlignment(Qt.AlignCenter)  # Center the logo
        self.layout.addWidget(logo_label, alignment=Qt.AlignCenter)

    def init_ui(self):
        # Create a label
        label = QLabel("Create Timetable for:")
        label.setFont(QFont("Arial", 24, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        # Create buttons for Morning and Evening options
        morning_btn = QPushButton("Morning Classes")
        evening_btn = QPushButton("Evening Classes")

        # Set button styles
        button_style = """
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 10px;
                padding: 10px;  /* Reduced height */
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
        morning_btn.setStyleSheet(button_style)
        evening_btn.setStyleSheet(button_style)

            # Set button sizes
        morning_btn.setFixedSize(300, 60)
        evening_btn.setFixedSize(300, 60)

            # Set layout spacing
        self.layout.setSpacing(3)

        # Add buttons and spacer to the layout
        self.layout.addWidget(morning_btn, alignment=Qt.AlignCenter)
        self.layout.addWidget(evening_btn, alignment=Qt.AlignCenter)

        # Connect buttons to their respective functions
        morning_btn.clicked.connect(self.create_morning_timetable)
        evening_btn.clicked.connect(self.create_evening_timetable)

    def create_morning_timetable(self):
        self.check_and_open_timetable("morning_timetable.db")

    def create_evening_timetable(self):
        self.check_and_open_timetable("evening_timetable.db")

    def check_and_open_timetable(self, db_name):
        # Check if the database file exists
        if not os.path.exists(db_name):
            # Create the database if it doesn't exist
            database.create_database(db_name)
            QMessageBox.information(self, "Database Created", f"Database '{db_name}' has been created.")
        
        # Open the timetable creation window
        self.timetable_window = TimetableCreationWindow(db_name)
        self.timetable_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

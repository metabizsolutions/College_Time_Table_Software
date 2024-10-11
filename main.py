import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QMessageBox, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import database  # Assuming this is your database.py file with the create_database function


def fetch_data_from_database(query):
    """Helper function to fetch data from the timetable.db."""
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


class TimetableCreationWindow(QWidget):
    def __init__(self, db_name, timetable_type):
        super().__init__()
        self.setWindowTitle(f"Create {timetable_type} Timetable")
        self.setGeometry(100, 100, 1280, 720)

        # Set background color for the window
        self.setStyleSheet("background-color: #49bcfc;")

        layout = QVBoxLayout(self)

        # Add logo in the center
        self.add_logo(layout)

        # Header label
        label = QLabel(f"Create {timetable_type} Timetable")
        label.setFont(QFont("Arial", 24, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")  # Set label text color to white for visibility
        layout.addWidget(label)

        # Add form fields
        self.add_form_fields(layout)

        self.setLayout(layout)

    def add_logo(self, layout):
        """Adds the logo to the window."""
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")  # Load the logo image
        logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio))  # Scale the logo
        logo_label.setAlignment(Qt.AlignCenter)  # Center the logo
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

    def add_form_fields(self, layout):
        """Adds form fields and populates them with data from the database."""
        # Fetch data from the database
        classrooms = fetch_data_from_database("SELECT classroom_name FROM Classrooms")
        teachers = fetch_data_from_database("SELECT teacher_name FROM Teachers")
        courses = fetch_data_from_database("SELECT course_name, course_code FROM Courses")
        programs = fetch_data_from_database("SELECT program_name, semester FROM Programs")

        # Create a horizontal layout for each row of input fields
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        
        # Create and populate the dropdowns for the first row
        self.classroom_combobox = self.create_combobox("Select Classroom", [classroom[0] for classroom in classrooms], hbox1)
        self.teacher_combobox = self.create_combobox("Select Teacher", [teacher[0] for teacher in teachers], hbox1)
        self.course_combobox = self.create_combobox("Select Course Title", [course[0] for course in courses], hbox1)

        # Create and populate the dropdowns for the second row
        self.code_combobox = self.create_combobox("Select Code", [course[1] for course in courses], hbox2)
        self.program_combobox = self.create_combobox("Select Program", [program[0] for program in programs], hbox2)
        self.semester_combobox = self.create_combobox("Select Semester", [program[1] for program in programs], hbox2)

        # Add both horizontal layouts to the main layout
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)

    def create_combobox(self, label_text, items, layout):
        """Helper function to create a ComboBox with label and populate items."""
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        combobox = QComboBox()
        combobox.setFont(QFont("Arial", 14))
        for item in items:
            combobox.addItem(item)  # Add item to the ComboBox
        layout.addWidget(combobox)
        return combobox


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

        # Set background color
        self.central_widget.setStyleSheet("background-color: #49bcfc;")

        # Add logo in the center
        self.add_logo()

        # Styling the window and buttons
        self.init_ui()

    def add_logo(self):
        """Adds the logo to the main window."""
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")  # Load the logo image
        logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio))  # Scale the logo
        logo_label.setAlignment(Qt.AlignCenter)  # Center the logo
        self.layout.addWidget(logo_label, alignment=Qt.AlignCenter)

    def init_ui(self):
        # Create a label
        label = QLabel("Create Timetable")
        label.setFont(QFont("Georgia", 24, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        # Create buttons for Morning and Evening options
        morning_btn = QPushButton("Morning Classes")
        evening_btn = QPushButton("Evening Classes")

        # Set button styles
        button_style = """
            QPushButton {
                background-color: #181818;
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

        # Change the font of the buttons
        button_font = QFont("Georgia", 16, QFont.Bold)
        morning_btn.setFont(button_font)
        evening_btn.setFont(button_font)

        # Set button sizes
        morning_btn.setFixedSize(300, 60)
        evening_btn.setFixedSize(300, 60)

        # Set layout spacing
        self.layout.setSpacing(3)

        # Add buttons to the layout
        self.layout.addWidget(morning_btn, alignment=Qt.AlignCenter)
        self.layout.addWidget(evening_btn, alignment=Qt.AlignCenter)

        # Connect buttons to their respective functions
        morning_btn.clicked.connect(lambda: self.create_timetable("Morning"))
        evening_btn.clicked.connect(lambda: self.create_timetable("Evening"))

        # Create a label
        label = QLabel("Developed by: MetaBiz Solution")
        label.setFont(QFont("Georgia", 15, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

    def create_timetable(self, timetable_type):
        # Check and open timetable using the single database "timetable.db"
        db_name = "timetable.db"
        self.check_and_open_timetable(db_name, timetable_type)

    def check_and_open_timetable(self, db_name, timetable_type):
        # Check if the database file exists
        if not os.path.exists(db_name):
            # Create the database if it doesn't exist
            database.create_database(db_name)
            QMessageBox.information(self, "Database Created", f"Database '{db_name}' has been created.")
        
        # Open the timetable creation window
        self.timetable_window = TimetableCreationWindow(db_name, timetable_type)
        self.timetable_window.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.showMaximized()
    sys.exit(app.exec_())

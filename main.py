import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog, QComboBox, QTableView, QAbstractItemView
from PyQt5.QtCore import QAbstractTableModel, Qt
import sqlite3

# Function to connect to SQLite and create the necessary tables
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create tables for Programs, Courses, Teachers, etc.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Programs (
        program_id INTEGER PRIMARY KEY,
        program_name TEXT NOT NULL,
        semester TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        course_code TEXT NOT NULL,
        credits TEXT NOT NULL,
        program_id INTEGER,
        FOREIGN KEY(program_id) REFERENCES Programs(program_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY,
        teacher_name TEXT NOT NULL,
        bps_grade INTEGER NOT NULL,
        specialization TEXT
    )
    ''')

    # Add more table creation queries here if needed
    conn.commit()
    conn.close()


# Model for displaying timetable in QTableView
class TimetableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            headers = ["Day", "Period", "Course", "Teacher", "Classroom"]
            if orientation == Qt.Horizontal:
                return headers[section]


# Class for Class Timetable window
class ClassTimetable(QDialog):
    def __init__(self, db_name):
        super().__init__()
        self.setWindowTitle("Class Timetable")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Label and dropdown for selecting class/semester
        self.label = QLabel("Select Class:")
        self.class_dropdown = QComboBox()
        # Dummy data for dropdown, you can populate it from the database later
        self.class_dropdown.addItems(["BS Chemistry", "BS Physics", "BS Zoology"])

        # Timetable display area (QTableView)
        self.table_view = QTableView()
        self.table_view.setSelectionMode(QAbstractItemView.NoSelection)

        # Generate button
        self.generate_btn = QPushButton("Generate Timetable")
        self.generate_btn.clicked.connect(self.generate_timetable)

        layout.addWidget(self.label)
        layout.addWidget(self.class_dropdown)
        layout.addWidget(self.table_view)
        layout.addWidget(self.generate_btn)

        self.setLayout(layout)
        self.db_name = db_name

    def generate_timetable(self):
        # Query database and generate timetable data here (dummy data for now)
        data = [
            ['Monday', '08:00-08:40', 'Plant Biochemistry', 'Mr. Shafi', 'S-13'],
            ['Monday', '08:40-09:20', 'Organic Chemistry', 'Mr. Imran', 'S-13'],
            ['Tuesday', '08:00-08:40', 'Entrepreneurship', 'Mr. Shoaib', 'S-13']
        ]

        model = TimetableModel(data)
        self.table_view.setModel(model)


# Main Window for timetable management after selecting Morning/Evening
class MainWindow(QMainWindow):
    def __init__(self, db_name):
        super().__init__()
        self.setWindowTitle("Timetable Management System")
        self.setGeometry(100, 100, 1280, 720)

        # Create and connect to the database on startup
        self.db_name = db_name
        create_database(self.db_name)

        # Layout for main window buttons
        layout = QVBoxLayout()

        # Buttons for timetable options
        class_timetable_btn = QPushButton("Generate Class Timetable")
        dept_timetable_btn = QPushButton("Generate Department Timetable")
        teacher_timetable_btn = QPushButton("Generate Teacher Timetable (with Workload)")
        overall_timetable_btn = QPushButton("Generate Overall College Timetable")

        # Connect buttons to corresponding functions
        class_timetable_btn.clicked.connect(self.open_class_timetable)

        layout.addWidget(class_timetable_btn)
        layout.addWidget(dept_timetable_btn)
        layout.addWidget(teacher_timetable_btn)
        layout.addWidget(overall_timetable_btn)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_class_timetable(self):
        self.class_timetable_window = ClassTimetable(self.db_name)
        self.class_timetable_window.show()


# Initial Selection Window to choose between Morning or Evening classes
class SelectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Class Type")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        # Label for selection
        self.label = QLabel("Select Class Type (Morning/Evening):")
        layout.addWidget(self.label)

        # Buttons for selection
        morning_btn = QPushButton("Morning Classes")
        evening_btn = QPushButton("Evening Classes")
        layout.addWidget(morning_btn)
        layout.addWidget(evening_btn)

        # Connect buttons to functions
        morning_btn.clicked.connect(self.start_morning_timetable)
        evening_btn.clicked.connect(self.start_evening_timetable)

        # Set layout and show window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_morning_timetable(self):
        self.launch_main_app("morning_timetable.db")

    def start_evening_timetable(self):
        self.launch_main_app("evening_timetable.db")

    def launch_main_app(self, db_name):
        self.close()  # Close the selection window
        self.main_window = MainWindow(db_name)  # Open the main window with the selected DB
        self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    selection_window = SelectionWindow()
    selection_window.show()
    sys.exit(app.exec_())

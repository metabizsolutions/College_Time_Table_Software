import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import database  # Ensure this imports your database functions correctly


class ViewTimetableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Timetable")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_timetable()

    def load_timetable(self):
        timetable_data = database.fetch_data("SELECT * FROM Schedule")  # Assuming you want to view the Schedule table
        self.populate_table(timetable_data)

    def populate_table(self, data):
        if data:
            self.table_widget.setColumnCount(len(data[0]))
            self.table_widget.setRowCount(len(data))
            self.table_widget.setHorizontalHeaderLabels(
                ["ID", "Classroom", "Teacher", "Course", "Program", "Semester"]
            )  # Adjust according to your Schedule columns

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.table_widget.resizeColumnsToContents()


class AddDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Data")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        # Add form fields for adding new data (e.g., classrooms, teachers, etc.)
        self.classroom_combobox = self.create_combobox("Select Classroom", self.fetch_classrooms())
        self.teacher_combobox = self.create_combobox("Select Teacher", self.fetch_teachers())
        self.course_combobox = self.create_combobox("Select Course", self.fetch_courses())
        self.program_combobox = self.create_combobox("Select Program", self.fetch_programs())

        self.add_button = QPushButton("Add Data")
        self.add_button.clicked.connect(self.add_data)

        self.layout.addWidget(self.classroom_combobox)
        self.layout.addWidget(self.teacher_combobox)
        self.layout.addWidget(self.course_combobox)
        self.layout.addWidget(self.program_combobox)
        self.layout.addWidget(self.add_button)

    def create_combobox(self, label_text, items):
        combobox = QComboBox()
        combobox.addItems(items)
        return combobox

    def fetch_classrooms(self):
        classrooms = database.fetch_data("SELECT classroom_name FROM Classrooms")
        return [classroom[0] for classroom in classrooms]

    def fetch_teachers(self):
        teachers = database.fetch_data("SELECT teacher_name FROM Teachers")
        return [teacher[0] for teacher in teachers]

    def fetch_courses(self):
        courses = database.fetch_data("SELECT course_name FROM Courses")
        return [course[0] for course in courses]

    def fetch_programs(self):
        programs = database.fetch_data("SELECT program_name FROM Programs")
        return [program[0] for program in programs]

    def add_data(self):
        # Logic to add data to the database based on the selected values
        # You can add more logic to insert data into the respective tables
        pass


class UpdateDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Data")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_data()

    def load_data(self):
        all_data = database.fetch_data("SELECT * FROM Schedule")  # Load data from Schedule table
        self.populate_table(all_data)

    def populate_table(self, data):
        if data:
            self.table_widget.setColumnCount(len(data[0]))
            self.table_widget.setRowCount(len(data))
            self.table_widget.setHorizontalHeaderLabels(
                ["ID", "Classroom", "Teacher", "Course", "Program", "Semester"]
            )  # Adjust according to your Schedule columns

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.table_widget.resizeColumnsToContents()


class TimetableSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Timetable")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        self.morning_button = QPushButton("Morning Timetable")
        self.evening_button = QPushButton("Evening Timetable")

        # Set button styles
        button_style = """
            QPushButton {
                background-color: #181818;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
        for button in [self.morning_button, self.evening_button]:
            button.setStyleSheet(button_style)
            button.setFont(QFont("Georgia", 18, QFont.Bold))
            button.setFixedSize(300, 60)

        self.layout.addWidget(self.morning_button)
        self.layout.addWidget(self.evening_button)

        self.setLayout(self.layout)

        # Connect buttons to their functions
        self.morning_button.clicked.connect(self.create_morning_timetable)
        self.evening_button.clicked.connect(self.create_evening_timetable)

    def create_morning_timetable(self):
        # Logic to create morning timetable
        print("Creating morning timetable...")

    def create_evening_timetable(self):
        # Logic to create evening timetable
        print("Creating evening timetable...")


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Timetable Management System")
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #49bcfc;")

        self.add_logo()
        self.init_ui()

    def add_logo(self):
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")  # Load logo image
        logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label, alignment=Qt.AlignCenter)

    def init_ui(self):
        label = QLabel("Create Timetable")
        label.setFont(QFont("Georgia", 28, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        # Main buttons
        view_btn = QPushButton("View Timetable")
        add_btn = QPushButton("Add New Data")
        update_btn = QPushButton("Update Data")
        create_btn = QPushButton("Create Timetable")

        button_style = """
            QPushButton {
                background-color: #181818;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
        for btn in [view_btn, add_btn, update_btn, create_btn]:
            btn.setStyleSheet(button_style)
            btn.setFont(QFont("Georgia", 18, QFont.Bold))
            btn.setFixedSize(300, 60)

        self.layout.addWidget(view_btn, alignment=Qt.AlignCenter)
        self.layout.addWidget(add_btn, alignment=Qt.AlignCenter)
        self.layout.addWidget(update_btn, alignment=Qt.AlignCenter)
        self.layout.addWidget(create_btn, alignment=Qt.AlignCenter)

        view_btn.clicked.connect(self.open_view_timetable)
        add_btn.clicked.connect(self.open_add_data)
        update_btn.clicked.connect(self.open_update_data)
        create_btn.clicked.connect(self.open_create_timetable)

        # Add footer
        self.add_footer()

    def add_footer(self):
        footer_label = QLabel("Developed by MetaBiz Solutions")
        footer_label.setFont(QFont("Georgia", 12, QFont.Bold))
        footer_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(footer_label, alignment=Qt.AlignCenter)

    def open_view_timetable(self):
        self.view_window = ViewTimetableWindow()
        self.view_window.show()

    def open_add_data(self):
        self.add_window = AddDataWindow()
        self.add_window.show()

    def open_update_data(self):
        self.update_window = UpdateDataWindow()
        self.update_window.show()

    def open_create_timetable(self):
        self.timetable_selection_window = TimetableSelectionWindow()
        self.timetable_selection_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

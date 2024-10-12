import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import sqlite3

# Database function to execute queries
def execute_query(query, parameters=()):
    connection = sqlite3.connect("timetable.db")  # Ensure this is your correct database file
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()

# Window for viewing timetable selections
class ViewTimetableSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Timetable")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Sample content for the window
        self.label = QLabel("Select a Timetable to View")
        self.label.setFont(QFont("Georgia", 24, QFont.Bold))
        self.layout.addWidget(self.label)

        # Example buttons for timetable selection (modify as needed)
        self.class_timetable_btn = QPushButton("Class Timetable")
        self.exam_timetable_btn = QPushButton("Exam Timetable")

        for btn in [self.class_timetable_btn, self.exam_timetable_btn]:
            btn.setFont(QFont("Georgia", 18, QFont.Bold))
            btn.setFixedSize(250, 50)
            self.layout.addWidget(btn)

# Window for adding classrooms
class AddClassroomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Classroom")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout(self)

        self.classroom_input = QLineEdit(self)
        self.classroom_input.setPlaceholderText("Enter Classroom Name")
        self.layout.addWidget(self.classroom_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFont(QFont("Georgia", 16, QFont.Bold))
        self.submit_btn.clicked.connect(self.add_classroom)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

    def add_classroom(self):
        classroom_name = self.classroom_input.text()
        if classroom_name:
            query = "INSERT INTO Classrooms (classroom_name) VALUES (?)"
            execute_query(query, (classroom_name,))
            self.close()

# Window for adding courses
class AddCourseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Course")
        self.setGeometry(100, 100, 300, 300)
        self.layout = QVBoxLayout(self)

        self.course_name_input = QLineEdit(self)
        self.course_code_input = QLineEdit(self)
        self.credits_input = QLineEdit(self)

        self.course_name_input.setPlaceholderText("Enter Course Name")
        self.course_code_input.setPlaceholderText("Enter Course Code")
        self.credits_input.setPlaceholderText("Enter Credits")

        self.layout.addWidget(self.course_name_input)
        self.layout.addWidget(self.course_code_input)
        self.layout.addWidget(self.credits_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFont(QFont("Georgia", 16, QFont.Bold))
        self.submit_btn.clicked.connect(self.add_course)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

    def add_course(self):
        course_name = self.course_name_input.text()
        course_code = self.course_code_input.text()
        credits = self.credits_input.text()
        if course_name and course_code and credits:
            query = "INSERT INTO Courses (course_name, course_code, credits) VALUES (?, ?, ?)"
            execute_query(query, (course_name, course_code, credits))
            self.close()

# Window for adding days
class AddDayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Day")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout(self)

        self.day_input = QLineEdit(self)
        self.day_input.setPlaceholderText("Enter Day Name")
        self.layout.addWidget(self.day_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFont(QFont("Georgia", 16, QFont.Bold))
        self.submit_btn.clicked.connect(self.add_day)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

    def add_day(self):
        day_name = self.day_input.text()
        if day_name:
            query = "INSERT INTO Days (day_name) VALUES (?)"
            execute_query(query, (day_name,))
            self.close()

# Window for adding programs
class AddProgramWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Program")
        self.setGeometry(100, 100, 300, 300)
        self.layout = QVBoxLayout(self)

        self.program_name_input = QLineEdit(self)
        self.semester_input = QLineEdit(self)

        self.program_name_input.setPlaceholderText("Enter Program Name")
        self.semester_input.setPlaceholderText("Enter Semester")

        self.layout.addWidget(self.program_name_input)
        self.layout.addWidget(self.semester_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFont(QFont("Georgia", 16, QFont.Bold))
        self.submit_btn.clicked.connect(self.add_program)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

    def add_program(self):
        program_name = self.program_name_input.text()
        semester = self.semester_input.text()
        if program_name and semester:
            query = "INSERT INTO Programs (program_name, semester) VALUES (?, ?)"
            execute_query(query, (program_name, semester))
            self.close()

# Window for adding teachers
class AddTeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Teacher")
        self.setGeometry(100, 100, 300, 300)
        self.layout = QVBoxLayout(self)

        self.teacher_name_input = QLineEdit(self)
        self.bps_grade_input = QLineEdit(self)
        self.specialization_input = QLineEdit(self)

        self.teacher_name_input.setPlaceholderText("Enter Teacher Name")
        self.bps_grade_input.setPlaceholderText("Enter BPS Grade")
        self.specialization_input.setPlaceholderText("Enter Specialization")

        self.layout.addWidget(self.teacher_name_input)
        self.layout.addWidget(self.bps_grade_input)
        self.layout.addWidget(self.specialization_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFont(QFont("Georgia", 16, QFont.Bold))
        self.submit_btn.clicked.connect(self.add_teacher)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

    def add_teacher(self):
        teacher_name = self.teacher_name_input.text()
        bps_grade = self.bps_grade_input.text()
        specialization = self.specialization_input.text()
        if teacher_name and bps_grade and specialization:
            query = "INSERT INTO Teachers (teacher_name, bps_grade, specialization) VALUES (?, ?, ?)"
            execute_query(query, (teacher_name, bps_grade, specialization))
            self.close()

# Main application window
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Timetable Management System")
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #49bcfc;")

        self.button_style = """
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
        """  # Define button style here

        self.add_logo()
        self.init_ui()

        # Store window instances to avoid recreating them
        self.view_selection_window = None
        self.add_data_window = None
        self.update_data_window = None
        self.create_timetable_window = None

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

        self.view_timetable_btn = QPushButton("View Timetable")
        self.create_timetable_btn = QPushButton("Create Timetable")
        self.add_data_btn = QPushButton("Add Data")
        self.update_data_btn = QPushButton("Update Data")
        
        for btn in [self.view_timetable_btn, self.create_timetable_btn, self.add_data_btn, self.update_data_btn]:
            btn.setStyleSheet(self.button_style)  # Use self.button_style
            btn.setFont(QFont("Georgia", 16, QFont.Bold))
            btn.setFixedSize(250, 50)
            self.layout.addWidget(btn, alignment=Qt.AlignCenter)

        self.view_timetable_btn.clicked.connect(self.open_view_timetable_selection)
        self.create_timetable_btn.clicked.connect(self.open_create_timetable)
        self.add_data_btn.clicked.connect(self.open_add_data)
        self.update_data_btn.clicked.connect(self.open_update_data)

    def open_view_timetable_selection(self):
        if self.view_selection_window is None or not self.view_selection_window.isVisible():
            self.view_selection_window = ViewTimetableSelectionWindow()
            self.view_selection_window.show()

    def open_create_timetable(self):
        if self.create_timetable_window is None or not self.create_timetable_window.isVisible():
            self.create_timetable_window = QWidget()
            self.create_timetable_window.setWindowTitle("Create Timetable")
            self.create_timetable_window.setGeometry(100, 100, 400, 300)
            self.create_timetable_window.setStyleSheet("background-color: #49bcfc;")
            self.create_timetable_window.show()

    def open_add_data(self):
        if self.add_data_window is None:
            self.add_data_window = QWidget()
            self.add_data_window.setWindowTitle("Add Data")
            self.add_data_window.setGeometry(100, 100, 300, 300)
            self.add_data_window.setStyleSheet("background-color: #49bcfc;")

            # Layout for buttons to add different entities
            add_layout = QVBoxLayout(self.add_data_window)

            add_classroom_btn = QPushButton("Add Classroom")
            add_course_btn = QPushButton("Add Course")
            add_day_btn = QPushButton("Add Day")
            add_program_btn = QPushButton("Add Program")
            add_teacher_btn = QPushButton("Add Teacher")

            for btn in [add_classroom_btn, add_course_btn, add_day_btn, add_program_btn, add_teacher_btn]:
                btn.setStyleSheet(self.button_style)  # Use self.button_style
                btn.setFont(QFont("Georgia", 16, QFont.Bold))
                btn.setFixedSize(250, 50)
                add_layout.addWidget(btn, alignment=Qt.AlignCenter)

            # Connect buttons with proper window handling
            add_classroom_btn.clicked.connect(self.show_add_classroom_window)
            add_course_btn.clicked.connect(lambda: AddCourseWindow().show())
            add_day_btn.clicked.connect(lambda: AddDayWindow().show())
            add_program_btn.clicked.connect(lambda: AddProgramWindow().show())
            add_teacher_btn.clicked.connect(lambda: AddTeacherWindow().show())

            self.add_data_window.setLayout(add_layout)
            self.add_data_window.show()
        else:
            self.add_data_window.activateWindow()  # Bring the existing window to the front

    def show_add_classroom_window(self):
        if self.add_classroom_window is None or not self.add_classroom_window.isVisible():
            self.add_classroom_window = AddClassroomWindow()
            self.add_classroom_window.show()
        else:
            self.add_classroom_window.activateWindow()  # Bring the existing window to the front

    def open_update_data(self):
        if self.update_data_window is None:
            self.update_data_window = QWidget()
            self.update_data_window.setWindowTitle("Update Data")
            self.update_data_window.setGeometry(100, 100, 400, 300)
            self.update_data_window.setStyleSheet("background-color: #49bcfc;")
            self.update_data_window.show()
        else:
            self.update_data_window.activateWindow()  # Bring the existing window to the front

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

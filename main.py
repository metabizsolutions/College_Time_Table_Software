import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import database  # Ensure this imports your database functions correctly

class AddDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Data")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        self.add_classroom_btn = QPushButton("Add Classrooms")
        self.add_courses_btn = QPushButton("Add Courses")
        self.add_days_btn = QPushButton("Add Days")
        self.add_programs_btn = QPushButton("Add Programs")
        self.add_teacher_btn = QPushButton("Add Teacher")

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
        for button in [self.add_classroom_btn, self.add_courses_btn, self.add_days_btn, self.add_programs_btn, self.add_teacher_btn]:
            button.setStyleSheet(button_style)
            button.setFont(QFont("Georgia", 18, QFont.Bold))
            button.setFixedSize(300, 60)

        self.layout.addWidget(self.add_classroom_btn)
        self.layout.addWidget(self.add_courses_btn)
        self.layout.addWidget(self.add_days_btn)
        self.layout.addWidget(self.add_programs_btn)
        self.layout.addWidget(self.add_teacher_btn)

        self.setLayout(self.layout)

        # Connect buttons to their functions
        self.add_classroom_btn.clicked.connect(self.open_add_classroom)
        self.add_courses_btn.clicked.connect(self.open_add_courses)
        self.add_days_btn.clicked.connect(self.open_add_days)
        self.add_programs_btn.clicked.connect(self.open_add_programs)
        self.add_teacher_btn.clicked.connect(self.open_add_teacher)

    def open_add_classroom(self):
        self.classroom_window = AddClassroomWindow()
        self.classroom_window.show()

    def open_add_courses(self):
        self.courses_window = AddCoursesWindow()
        self.courses_window.show()

    def open_add_days(self):
        self.days_window = AddDaysWindow()
        self.days_window.show()

    def open_add_programs(self):
        self.programs_window = AddProgramsWindow()
        self.programs_window.show()

    def open_add_teacher(self):
        self.teacher_window = AddTeacherWindow()
        self.teacher_window.show()


# Individual windows for each data type

class AddClassroomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Classroom")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter Classroom Name:")
        self.layout.addWidget(self.label)

        self.classroom_input = QLineEdit()
        self.layout.addWidget(self.classroom_input)

        self.submit_btn = QPushButton("Submit")
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

        # Connect the submit button to store data
        self.submit_btn.clicked.connect(self.submit_classroom)

    def submit_classroom(self):
        classroom_name = self.classroom_input.text()
        query = "INSERT INTO Classrooms (classroom_name) VALUES (?)"
        database.execute_query(query, (classroom_name,))
        self.close()


class AddCoursesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Courses")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        self.course_name_label = QLabel("Course Name:")
        self.layout.addWidget(self.course_name_label)
        self.course_name_input = QLineEdit()
        self.layout.addWidget(self.course_name_input)

        self.course_code_label = QLabel("Course Code:")
        self.layout.addWidget(self.course_code_label)
        self.course_code_input = QLineEdit()
        self.layout.addWidget(self.course_code_input)

        self.credits_label = QLabel("Credits:")
        self.layout.addWidget(self.credits_label)
        self.credits_input = QLineEdit()
        self.layout.addWidget(self.credits_input)

        self.submit_btn = QPushButton("Submit")
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

        # Connect the submit button to store data
        self.submit_btn.clicked.connect(self.submit_course)

    def submit_course(self):
        course_name = self.course_name_input.text()
        course_code = self.course_code_input.text()
        credits = self.credits_input.text()
        query = "INSERT INTO Courses (course_name, course_code, credits) VALUES (?, ?, ?)"
        database.execute_query(query, (course_name, course_code, credits))
        self.close()


class AddDaysWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Days")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter Day Name:")
        self.layout.addWidget(self.label)

        self.day_input = QLineEdit()
        self.layout.addWidget(self.day_input)

        self.submit_btn = QPushButton("Submit")
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

        # Connect the submit button to store data
        self.submit_btn.clicked.connect(self.submit_day)

    def submit_day(self):
        day_name = self.day_input.text()
        query = "INSERT INTO Days (day_name) VALUES (?)"
        database.execute_query(query, (day_name,))
        self.close()


class AddProgramsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Programs")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        self.program_name_label = QLabel("Program Name:")
        self.layout.addWidget(self.program_name_label)
        self.program_name_input = QLineEdit()
        self.layout.addWidget(self.program_name_input)

        self.semester_label = QLabel("Semester:")
        self.layout.addWidget(self.semester_label)
        self.semester_input = QLineEdit()
        self.layout.addWidget(self.semester_input)

        self.submit_btn = QPushButton("Submit")
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

        # Connect the submit button to store data
        self.submit_btn.clicked.connect(self.submit_program)

    def submit_program(self):
        program_name = self.program_name_input.text()
        semester = self.semester_input.text()
        query = "INSERT INTO Programs (program_name, semester) VALUES (?, ?)"
        database.execute_query(query, (program_name, semester))
        self.close()


class AddTeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Teacher")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        self.teacher_name_label = QLabel("Teacher Name:")
        self.layout.addWidget(self.teacher_name_label)
        self.teacher_name_input = QLineEdit()
        self.layout.addWidget(self.teacher_name_input)

        self.bps_label = QLabel("BPS Grade:")
        self.layout.addWidget(self.bps_label)
        self.bps_input = QLineEdit()
        self.layout.addWidget(self.bps_input)

        self.specialization_label = QLabel("Specialization:")
        self.layout.addWidget(self.specialization_label)
        self.specialization_input = QLineEdit()
        self.layout.addWidget(self.specialization_input)

        self.submit_btn = QPushButton("Submit")
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

        # Connect the submit button to store data
        self.submit_btn.clicked.connect(self.submit_teacher)

    def submit_teacher(self):
        teacher_name = self.teacher_name_input.text()
        bps = self.bps_input.text()
        specialization = self.specialization_input.text()
        query = "INSERT INTO Teachers (teacher_name, bps, specialization) VALUES (?, ?, ?)"
        database.execute_query(query, (teacher_name, bps, specialization))
        self.close()


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
        logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFixedSize(150, 150)
        self.layout.addWidget(logo_label)

    def init_ui(self):
        label = QLabel("Timetable Management System")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #1d1d1d;")
        label.setFont(QFont("Georgia", 28, QFont.Bold))
        self.layout.addWidget(label)

        button_layout = QVBoxLayout()

        self.add_new_data_btn = QPushButton("Add New Data")
        self.create_timetable_btn = QPushButton("Create Timetable")
        self.view_timetable_btn = QPushButton("View Timetable")
        self.update_data_btn = QPushButton("Update Data")

        buttons = [self.add_new_data_btn, self.create_timetable_btn, self.view_timetable_btn, self.update_data_btn]
        for button in buttons:
            button.setStyleSheet("""
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
            """)
            button.setFont(QFont("Georgia", 18, QFont.Bold))
            button.setFixedSize(300, 60)
            button_layout.addWidget(button)

        self.layout.addLayout(button_layout)

        # Connect buttons to their respective windows
        self.add_new_data_btn.clicked.connect(self.open_add_data_window)

    def open_add_data_window(self):
        self.add_data_window = AddDataWindow()
        self.add_data_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

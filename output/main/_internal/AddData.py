from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QFont
from database import execute_query  # Assuming this is the database function you're using

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

    def add_classroom(self):
        classroom_name = self.classroom_input.text()
        if classroom_name:
            query = "INSERT INTO Classrooms (classroom_name) VALUES (?)"
            execute_query(query, (classroom_name,))
            self.close()

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

    def add_course(self):
        course_name = self.course_name_input.text()
        course_code = self.course_code_input.text()
        credits = self.credits_input.text()
        if course_name and course_code and credits:
            query = "INSERT INTO Courses (course_name, course_code, credits) VALUES (?, ?, ?)"
            execute_query(query, (course_name, course_code, credits))
            self.close()

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

    def add_day(self):
        day_name = self.day_input.text()
        if day_name:
            query = "INSERT INTO Days (day_name) VALUES (?)"
            execute_query(query, (day_name,))
            self.close()

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

    def add_program(self):
        program_name = self.program_name_input.text()
        semester = self.semester_input.text()
        if program_name and semester:
            query = "INSERT INTO Programs (program_name, semester) VALUES (?, ?)"
            execute_query(query, (program_name, semester))
            self.close()

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

    def add_teacher(self):
        teacher_name = self.teacher_name_input.text()
        bps_grade = self.bps_grade_input.text()
        specialization = self.specialization_input.text()
        if teacher_name and bps_grade and specialization:
            query = "INSERT INTO Teachers (teacher_name, bps_grade, specialization) VALUES (?, ?, ?)"
            execute_query(query, (teacher_name, bps_grade, specialization))
            self.close()

class AddDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Data")
        self.setGeometry(100, 100, 400, 400)
        self.layout = QVBoxLayout(self)

        # Add buttons for different actions
        self.add_classroom_button = QPushButton("Add Classroom")
        self.add_classroom_button.setFont(QFont("Georgia", 14))
        self.add_classroom_button.clicked.connect(self.open_add_classroom_window)
        self.layout.addWidget(self.add_classroom_button)

        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.setFont(QFont("Georgia", 14))
        self.add_course_button.clicked.connect(self.open_add_course_window)
        self.layout.addWidget(self.add_course_button)

        self.add_day_button = QPushButton("Add Day")
        self.add_day_button.setFont(QFont("Georgia", 14))
        self.add_day_button.clicked.connect(self.open_add_day_window)
        self.layout.addWidget(self.add_day_button)

        self.add_program_button = QPushButton("Add Program")
        self.add_program_button.setFont(QFont("Georgia", 14))
        self.add_program_button.clicked.connect(self.open_add_program_window)
        self.layout.addWidget(self.add_program_button)

        self.add_teacher_button = QPushButton("Add Teacher")
        self.add_teacher_button.setFont(QFont("Georgia", 14))
        self.add_teacher_button.clicked.connect(self.open_add_teacher_window)
        self.layout.addWidget(self.add_teacher_button)

    def open_add_classroom_window(self):
        self.classroom_window = AddClassroomWindow()
        self.classroom_window.show()

    def open_add_course_window(self):
        self.course_window = AddCourseWindow()
        self.course_window.show()

    def open_add_day_window(self):
        self.day_window = AddDayWindow()
        self.day_window.show()

    def open_add_program_window(self):
        self.program_window = AddProgramWindow()
        self.program_window.show()

    def open_add_teacher_window(self):
        self.teacher_window = AddTeacherWindow()
        self.teacher_window.show()

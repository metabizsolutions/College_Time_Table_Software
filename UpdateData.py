from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class UpdateDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Data")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        # Label for update section
        self.label = QLabel("Update Data Here")
        self.layout.addWidget(self.label)

        # Buttons for different update options
        self.btn_update_classroom = QPushButton("Update Classroom")
        self.btn_update_courses = QPushButton("Update Courses")
        self.btn_update_program = QPushButton("Update Programs")
        self.btn_update_teachers = QPushButton("Update Teachers Data")

        # Add buttons to layout
        self.layout.addWidget(self.btn_update_classroom)
        self.layout.addWidget(self.btn_update_courses)
        self.layout.addWidget(self.btn_update_program)
        self.layout.addWidget(self.btn_update_teachers)

        # Connect buttons to their respective functions
        self.btn_update_classroom.clicked.connect(lambda: self.update_classroom())  # Example ID
        self.btn_update_courses.clicked.connect(lambda: self.update_courses(1))  # Example ID
        self.btn_update_program.clicked.connect(lambda: self.update_program(1))  # Example ID
        self.btn_update_teachers.clicked.connect(lambda: self.update_teacher(1))  # Example ID

        self.setLayout(self.layout)

    def fetch_data(self, query, params):
        # Implement this method to fetch data from the database
        pass

    def execute_query(self, query, params):
        # Implement this method to execute queries against the database
        pass

    def update_classroom(self):
        # Fetch the current data from the database
        #query = "SELECT classroom_name FROM Classrooms WHERE classroom_id = ?"
        #result = self.fetch_data(query, (classroom_id))  # Fetch based on classroom_id

        query = "SELECT classroom_name FROM Classrooms"
        result = self.fetch_data(query)  # Fetch based on classroom_id
        
        if result:
            self.classroom_input = QLineEdit(result[0])  # Set the fetched classroom name
            self.layout.addWidget(self.classroom_input)

            self.update_button_classroom = QPushButton("Update Classroom")
            self.layout.addWidget(self.update_button_classroom)
            self.update_button_classroom.clicked.connect(lambda: self.save_classroom_data())
        else:
            QMessageBox.warning(self, "Warning", "No data found for the given Classroom ID")

    def save_classroom_data(self, classroom_id):
        updated_classroom = self.classroom_input.text()
        query = "UPDATE Classrooms SET classroom_name = ? WHERE classroom_id = ?"
        if self.execute_query(query, (updated_classroom, classroom_id)):
            QMessageBox.information(self, "Success", "Classroom updated successfully!")

    def update_courses(self, course_id):
        # Fetch the current data from the database
        query = "SELECT course_name, course_code, credits FROM Courses WHERE course_id = ?"
        result = self.fetch_data(query, (course_id,))  # Fetch based on course_id
        
        if result:
            self.course_name_input = QLineEdit(result[0])  # Set fetched course name
            self.course_code_input = QLineEdit(result[1])  # Set fetched course code
            self.credits_input = QLineEdit(str(result[2]))  # Set fetched credits

            self.layout.addWidget(self.course_name_input)
            self.layout.addWidget(self.course_code_input)
            self.layout.addWidget(self.credits_input)

            self.update_button_course = QPushButton("Update Course")
            self.layout.addWidget(self.update_button_course)
            self.update_button_course.clicked.connect(lambda: self.save_course_data(course_id))
        else:
            QMessageBox.warning(self, "Warning", "No data found for the given Course ID")

    def save_course_data(self, course_id):
        updated_course_name = self.course_name_input.text()
        updated_course_code = self.course_code_input.text()
        updated_credits = int(self.credits_input.text())
        
        query = "UPDATE Courses SET course_name = ?, course_code = ?, credits = ? WHERE course_id = ?"
        if self.execute_query(query, (updated_course_name, updated_course_code, updated_credits, course_id)):
            QMessageBox.information(self, "Success", "Course updated successfully!")

    def update_program(self, program_id):
        # Fetch the current data from the database
        query = "SELECT program_name, semester FROM Programs WHERE program_id = ?"
        result = self.fetch_data(query, (program_id,))  # Fetch based on program_id
        
        if result:
            self.program_name_input = QLineEdit(result[0])  # Set fetched program name
            self.semester_input = QLineEdit(result[1])  # Set fetched semester

            self.layout.addWidget(self.program_name_input)
            self.layout.addWidget(self.semester_input)

            self.update_button_program = QPushButton("Update Program")
            self.layout.addWidget(self.update_button_program)
            self.update_button_program.clicked.connect(lambda: self.save_program_data(program_id))
        else:
            QMessageBox.warning(self, "Warning", "No data found for the given Program ID")

    def save_program_data(self, program_id):
        updated_program_name = self.program_name_input.text()
        updated_semester = self.semester_input.text()
        
        query = "UPDATE Programs SET program_name = ?, semester = ? WHERE program_id = ?"
        if self.execute_query(query, (updated_program_name, updated_semester, program_id)):
            QMessageBox.information(self, "Success", "Program updated successfully!")

    def update_teacher(self, teacher_id):
        # Fetch the current data from the database
        query = "SELECT teacher_name, bps_grade, specialization FROM Teachers WHERE teacher_id = ?"
        result = self.fetch_data(query, (teacher_id,))  # Fetch based on teacher_id
        
        if result:
            self.teacher_name_input = QLineEdit(result[0])  # Set fetched teacher name
            self.bps_grade_input = QLineEdit(result[1])  # Set fetched BPS Grade
            self.specialization_input = QLineEdit(result[2])  # Set fetched specialization

            self.layout.addWidget(self.teacher_name_input)
            self.layout.addWidget(self.bps_grade_input)
            self.layout.addWidget(self.specialization_input)

            self.update_button_teacher = QPushButton("Update Teacher")
            self.layout.addWidget(self.update_button_teacher)
            self.update_button_teacher.clicked.connect(lambda: self.save_teacher_data(teacher_id))
        else:
            QMessageBox.warning(self, "Warning", "No data found for the given Teacher ID")

    def save_teacher_data(self, teacher_id):
        updated_teacher_name = self.teacher_name_input.text()
        updated_bps_grade = self.bps_grade_input.text()
        updated_specialization = self.specialization_input.text()
        
        query = "UPDATE Teachers SET teacher_name = ?, bps_grade = ?, specialization = ? WHERE teacher_id = ?"
        if self.execute_query(query, (updated_teacher_name, updated_bps_grade, updated_specialization, teacher_id)):
            QMessageBox.information(self, "Success", "Teacher updated successfully!")

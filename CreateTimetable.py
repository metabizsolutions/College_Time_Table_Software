import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CreateTimetableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Timetable")
        self.setGeometry(100, 100, 400, 500)
        self.layout = QVBoxLayout(self)

        # Connect to the database
        self.conn = sqlite3.connect('timetable.db')
        self.cursor = self.conn.cursor()

        # Create input fields
        self.create_input_fields()

        # Add Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def create_input_fields(self):
        # Department selection
        self.department_label = QLabel("Select Department")
        self.department_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.department_label)

        self.department_combo = QComboBox()
        self.fetch_data("Programs", "program_name", self.department_combo)
        self.layout.addWidget(self.department_combo)

        # Semester selection
        self.semester_label = QLabel("Select Semester")
        self.semester_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.semester_label)

        self.semester_combo = QComboBox()
        self.fetch_data("Programs", "semester", self.semester_combo)
        self.layout.addWidget(self.semester_combo)

        # Teacher selection
        self.teacher_label = QLabel("Select Teacher")
        self.teacher_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.teacher_label)

        self.teacher_combo = QComboBox()
        self.fetch_data("Teachers", "teacher_name", self.teacher_combo)
        self.layout.addWidget(self.teacher_combo)

        # Course Title selection
        self.course_title_label = QLabel("Select Course Title")
        self.course_title_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.course_title_label)

        self.course_title_combo = QComboBox()
        self.fetch_data("Courses", "course_name", self.course_title_combo)
        self.layout.addWidget(self.course_title_combo)

        # Course Code selection
        self.course_code_label = QLabel("Select Course Code")
        self.course_code_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.course_code_label)

        self.course_code_combo = QComboBox()
        self.fetch_data("Courses", "course_code", self.course_code_combo)
        self.layout.addWidget(self.course_code_combo)

        # Classroom selection
        self.classroom_label = QLabel("Select Classroom")
        self.classroom_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.classroom_label)

        self.classroom_combo = QComboBox()
        self.fetch_data("Classrooms", "classroom_name", self.classroom_combo)
        self.layout.addWidget(self.classroom_combo)

        # Time input
        self.time_label = QLabel("Enter Time")
        self.time_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.time_label)

        self.time_input = QLineEdit()
        self.layout.addWidget(self.time_input)

        # Session selection (Morning/Evening)
        self.session_label = QLabel("Select Session")
        self.session_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.session_label)

        self.session_combo = QComboBox()
        self.session_combo.addItems(["Morning", "Evening"])
        self.layout.addWidget(self.session_combo)

    def fetch_data(self, table, column, combo_box):
        """Fetch data from the database and populate the combo box."""
        query = f"SELECT DISTINCT {column} FROM {table}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            combo_box.addItem(row[0])

    def submit_data(self):
        """Submit the selected data to the database."""
        department = self.department_combo.currentText()
        semester = self.semester_combo.currentText()
        teacher = self.teacher_combo.currentText()
        course_title = self.course_title_combo.currentText()
        course_code = self.course_code_combo.currentText()
        classroom = self.classroom_combo.currentText()
        time = self.time_input.text()
        session = self.session_combo.currentText()

        # Validate inputs
        if not time:
            QMessageBox.warning(self, "Input Error", "Please enter the lecture time.")
            return

        # Insert the data into a table (assuming you have a table for storing timetables)
        try:
            query = """
            INSERT INTO Timetable (department, semester, teacher, course_title, course_code, classroom, time, session)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (department, semester, teacher, course_title, course_code, classroom, time, session))
            self.conn.commit()

            QMessageBox.information(self, "Success", "Timetable created successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create timetable: {e}")

    def closeEvent(self, event):
        """Close the database connection when the window is closed."""
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = CreateTimetableWindow()
    window.show()
    sys.exit(app.exec_())

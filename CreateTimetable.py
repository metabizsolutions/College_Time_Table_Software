import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QListWidget, QComboBox, QTimeEdit
)
from PyQt5.QtCore import Qt, QTime
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
        # Department input
        self.department_label = QLabel("Search Department")
        self.department_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.department_label)

        self.department_input = QLineEdit(self)
        self.department_input.textChanged.connect(lambda: self.auto_complete("Programs", "program_name", self.department_input, self.department_list))
        self.layout.addWidget(self.department_input)

        self.department_list = QListWidget(self)
        self.department_list.itemClicked.connect(self.select_department)
        self.layout.addWidget(self.department_list)

        # Semester input
        self.semester_label = QLabel("Search Semester")
        self.semester_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.semester_label)

        self.semester_input = QLineEdit(self)
        self.semester_input.textChanged.connect(lambda: self.auto_complete("Programs", "semester", self.semester_input, self.semester_list))
        self.layout.addWidget(self.semester_input)

        self.semester_list = QListWidget(self)
        self.semester_list.itemClicked.connect(self.select_semester)
        self.layout.addWidget(self.semester_list)

        # Teacher input
        self.teacher_label = QLabel("Search Teacher")
        self.teacher_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.teacher_label)

        self.teacher_input = QLineEdit(self)
        self.teacher_input.textChanged.connect(lambda: self.auto_complete("Teachers", "teacher_name", self.teacher_input, self.teacher_list))
        self.layout.addWidget(self.teacher_input)

        self.teacher_list = QListWidget(self)
        self.teacher_list.itemClicked.connect(self.select_teacher)
        self.layout.addWidget(self.teacher_list)

        # Course Title input
        self.course_title_label = QLabel("Search Course Title")
        self.course_title_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.course_title_label)

        self.course_title_input = QLineEdit(self)
        self.course_title_input.textChanged.connect(lambda: self.auto_complete("Courses", "course_name", self.course_title_input, self.course_title_list))
        self.layout.addWidget(self.course_title_input)

        self.course_title_list = QListWidget(self)
        self.course_title_list.itemClicked.connect(self.select_course_title)
        self.layout.addWidget(self.course_title_list)

        # Course Code input
        self.course_code_label = QLabel("Search Course Code")
        self.course_code_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.course_code_label)

        self.course_code_input = QLineEdit(self)
        self.course_code_input.textChanged.connect(lambda: self.auto_complete("Courses", "course_code", self.course_code_input, self.course_code_list))
        self.layout.addWidget(self.course_code_input)

        self.course_code_list = QListWidget(self)
        self.course_code_list.itemClicked.connect(self.select_course_code)
        self.layout.addWidget(self.course_code_list)

        # Classroom input
        self.classroom_label = QLabel("Search Classroom")
        self.classroom_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.classroom_label)

        self.classroom_input = QLineEdit(self)
        self.classroom_input.textChanged.connect(lambda: self.auto_complete("Classrooms", "classroom_name", self.classroom_input, self.classroom_list))
        self.layout.addWidget(self.classroom_input)

        self.classroom_list = QListWidget(self)
        self.classroom_list.itemClicked.connect(self.select_classroom)
        self.layout.addWidget(self.classroom_list)

        # Lecture Start Time input using QTimeEdit
        self.start_time_label = QLabel("Select Lecture Start Time")
        self.start_time_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.start_time_label)

        self.start_time_input = QTimeEdit(self)
        self.start_time_input.setTime(QTime.currentTime())  # Set the current time as default
        self.layout.addWidget(self.start_time_input)

        # Lecture End Time input using QTimeEdit
        self.end_time_label = QLabel("Select Lecture End Time")
        self.end_time_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.end_time_label)

        self.end_time_input = QTimeEdit(self)
        self.end_time_input.setTime(QTime.currentTime())  # Set the current time as default
        self.layout.addWidget(self.end_time_input)

        # Session selection (Morning/Evening)
        self.session_label = QLabel("Select Session")
        self.session_label.setFont(QFont("Georgia", 14))
        self.layout.addWidget(self.session_label)

        self.session_combo = QComboBox()
        self.session_combo.addItems(["Morning", "Evening"])
        self.layout.addWidget(self.session_combo)

    def auto_complete(self, table, column, input_field, list_widget):
        """Perform a real-time search in the database and populate the list widget."""
        search_text = input_field.text()
        query = f"SELECT DISTINCT {column} FROM {table} WHERE {column} LIKE ?"
        self.cursor.execute(query, (f"%{search_text}%",))
        rows = self.cursor.fetchall()

        list_widget.clear()  # Clear the previous results
        for row in rows:
            list_widget.addItem(row[0])  # Add items to the list widget

    def select_department(self, item):
        """Set the selected department in the input field."""
        self.department_input.setText(item.text())
        self.department_list.clear()  # Clear the list after selection

    def select_semester(self, item):
        """Set the selected semester in the input field."""
        self.semester_input.setText(item.text())
        self.semester_list.clear()  # Clear the list after selection

    def select_teacher(self, item):
        """Set the selected teacher in the input field."""
        self.teacher_input.setText(item.text())
        self.teacher_list.clear()  # Clear the list after selection

    def select_course_title(self, item):
        """Set the selected course title in the input field."""
        self.course_title_input.setText(item.text())
        self.course_title_list.clear()  # Clear the list after selection

    def select_course_code(self, item):
        """Set the selected course code in the input field."""
        self.course_code_input.setText(item.text())
        self.course_code_list.clear()  # Clear the list after selection

    def select_classroom(self, item):
        """Set the selected classroom in the input field."""
        self.classroom_input.setText(item.text())
        self.classroom_list.clear()  # Clear the list after selection

    def submit_data(self):
        """Submit the selected data to the database."""
        department = self.department_input.text()
        semester = self.semester_input.text()
        teacher = self.teacher_input.text()
        course_title = self.course_title_input.text()
        course_code = self.course_code_input.text()
        classroom = self.classroom_input.text()
        start_time = self.start_time_input.time().toString('HH:mm')  # Get the selected start time
        end_time = self.end_time_input.time().toString('HH:mm')  # Get the selected end time
        session = self.session_combo.currentText()

        # Validate inputs
        if not department or not semester or not teacher or not course_title or not course_code or not classroom:
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return

        # Insert the data into the Timetable table
        try:
            query = """
            INSERT INTO Timetable (department, semester, teacher, course_title, course_code, classroom, lecture_start_time, lecture_end_time, session)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (department, semester, teacher, course_title, course_code, classroom, start_time, end_time, session))
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

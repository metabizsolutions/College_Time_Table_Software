import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QListWidget, QComboBox, QTimeEdit, QFormLayout, QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont

class CreateTimetableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Timetable")
        self.setGeometry(100, 100, 800, 600)

        # Connect to the database
        self.conn = sqlite3.connect('timetable.db')
        self.cursor = self.conn.cursor()

        # Main layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Scroll Area for the form
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area.setWidget(self.scroll_area_content)

        # Layout inside the scroll area
        self.form_layout = QFormLayout(self.scroll_area_content)

        # Initialize input fields
        self.department_input = QLineEdit(self)
        self.department_list = QListWidget(self)
        self.semester_input = QLineEdit(self)
        self.semester_list = QListWidget(self)
        self.teacher_input = QLineEdit(self)
        self.teacher_list = QListWidget(self)
        self.course_title_input = QLineEdit(self)
        self.course_title_list = QListWidget(self)
        self.course_code_input = QLineEdit(self)
        self.course_code_list = QListWidget(self)
        self.classroom_input = QLineEdit(self)
        self.classroom_list = QListWidget(self)
        self.start_time_input = QTimeEdit(self)
        self.end_time_input = QTimeEdit(self)
        self.session_combo = QComboBox()
        self.lecture_duration_input = QLineEdit(self)  # New field for lecture duration

        # Create input fields
        self.create_input_fields()

        # Add Scroll Area to main layout
        self.layout.addWidget(self.scroll_area)

        # Add Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

        self.showMaximized()

    def create_input_fields(self):
        # Department & Semester Section
        self.add_input_row("Department", "Search Department", self.department_input, self.department_list)
        self.add_input_row("Semester", "Search Semester", self.semester_input, self.semester_list)

        # Teacher & Course Title Section
        self.add_input_row("Teacher", "Search Teacher", self.teacher_input, self.teacher_list)
        self.add_input_row("Course Title", "Search Course Title", self.course_title_input, self.course_title_list)

        # Course Code Section
        self.add_input_row("Course Code", "Search Course Code", self.course_code_input, self.course_code_list)

        # Classroom Section
        self.add_input_row("Classroom", "Search Classroom", self.classroom_input, self.classroom_list)

        # Time Section: Start & End Time
        self.add_time_section()

        # Session Selection
        self.add_session_section()

        # Lecture Duration Section
        self.add_lecture_duration_section()

    def add_input_row(self, label, placeholder, input_field, list_widget):
        # Create input row with label, input field, and list box
        row_layout = QHBoxLayout()

        label_widget = QLabel(label)
        label_widget.setFont(QFont("Georgia", 14))
        row_layout.addWidget(label_widget)

        input_field.textChanged.connect(lambda: self.auto_complete(label, input_field, list_widget))
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedWidth(250)
        row_layout.addWidget(input_field)

        list_widget.setFixedWidth(950)
        list_widget.setFixedHeight(150)
        list_widget.itemClicked.connect(lambda item: self.select_item(input_field, list_widget, item))
        row_layout.addWidget(list_widget)

        self.form_layout.addRow(row_layout)

    def add_time_section(self):
        # Time section layout
        time_layout = QHBoxLayout()

        # Start Time
        start_time_label = QLabel("Select Lecture Start Time")
        start_time_label.setFont(QFont("Georgia", 12))
        self.start_time_input.setDisplayFormat("hh:mm AP")  # 12-hour format with AM/PM
        self.start_time_input.setTime(QTime.currentTime())
        time_layout.addWidget(start_time_label)
        time_layout.addWidget(self.start_time_input)

        # End Time
        end_time_label = QLabel("Select Lecture End Time")
        end_time_label.setFont(QFont("Georgia", 12))
        self.end_time_input.setDisplayFormat("hh:mm AP")  # 12-hour format with AM/PM
        self.end_time_input.setTime(QTime.currentTime())
        time_layout.addWidget(end_time_label)
        time_layout.addWidget(self.end_time_input)

        self.form_layout.addRow(time_layout)

    def add_session_section(self):
        session_layout = QHBoxLayout()
        
        session_label = QLabel("Select Session")
        session_label.setFont(QFont("Georgia", 14))
        session_layout.addWidget(session_label)

        self.session_combo.addItems(["Morning", "Evening"])
        session_layout.addWidget(self.session_combo)

        self.form_layout.addRow(session_layout)

    def add_lecture_duration_section(self):
        # Lecture duration layout
        duration_layout = QHBoxLayout()

        duration_label = QLabel("Lecture Duration (minutes)")
        duration_label.setFont(QFont("Georgia", 14))
        duration_layout.addWidget(duration_label)

        self.lecture_duration_input.setPlaceholderText("Enter duration in minutes")
        self.lecture_duration_input.setFixedWidth(250)
        duration_layout.addWidget(self.lecture_duration_input)

        self.form_layout.addRow(duration_layout)

    def auto_complete(self, label, input_field, list_widget):
        search_text = input_field.text()
        
        # Modify this function to query the correct table and column based on the field
        if label == "Department":
            query = """
            SELECT DISTINCT program_name FROM Programs WHERE program_name LIKE ?
            """
        elif label == "Semester":
            query = """
            SELECT DISTINCT semester FROM Programs WHERE semester LIKE ?
            """
        elif label == "Teacher":
            query = """
            SELECT DISTINCT teacher_name FROM Teachers WHERE teacher_name LIKE ?
            """
        elif label == "Course Title":
            query = """
            SELECT DISTINCT course_name FROM Courses WHERE course_name LIKE ?
            """
        elif label == "Course Code":
            query = """
            SELECT DISTINCT course_code FROM Courses WHERE course_code LIKE ?
            """
        elif label == "Classroom":
            query = """
            SELECT DISTINCT classroom_name FROM Classrooms WHERE classroom_name LIKE ?
            """
        else:
            return

        # Execute the query and fetch results
        self.cursor.execute(query, (f"%{search_text}%",))
        rows = self.cursor.fetchall()

        # Populate the list widget with fetched data
        list_widget.clear()
        for row in rows:
            list_widget.addItem(row[0])

    def select_item(self, input_field, list_widget, item):
        input_field.setText(item.text())
        list_widget.clear()

    def is_course_unique(self, course_title, course_code, department, semester):
        query = """
        SELECT * FROM Timetable 
        WHERE course_title = ? AND course_code = ? AND department = ? AND semester = ?
        """
        self.cursor.execute(query, (course_title, course_code, department, semester))
        return not bool(self.cursor.fetchall())  # Return True if the course is unique

    def submit_data(self):
        department = self.department_input.text()
        semester = self.semester_input.text()
        teacher = self.teacher_input.text()
        course_title = self.course_title_input.text()
        course_code = self.course_code_input.text()
        classroom = self.classroom_input.text()
        lecture_duration = self.lecture_duration_input.text()  # Get lecture duration

        start_time = self.start_time_input.time().toString('hh:mm AP')  # 12-hour format with AM/PM
        end_time = self.end_time_input.time().toString('hh:mm AP')  # 12-hour format with AM/PM

        session = self.session_combo.currentText()

        if not department or not semester or not teacher or not course_title or not course_code or not classroom or not lecture_duration:
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return

        if self.is_teacher_scheduled(teacher, start_time, end_time):
            QMessageBox.warning(self, "Schedule Conflict", f"This teacher is already scheduled during this time.")
            return

        if not self.is_course_unique(course_title, course_code, department, semester):
            QMessageBox.warning(self, "Course Conflict", f"This course title and code already exist for the selected department and semester.")
            return

        try:
            query = """
            INSERT INTO Timetable (department, semester, teacher, course_title, course_code, classroom, lecture_start_time, lecture_end_time, session, lecture_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (department, semester, teacher, course_title, course_code, classroom, start_time, end_time, session, lecture_duration))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Timetable entry created successfully!")
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

    def clear_inputs(self):
        self.department_input.clear()
        self.semester_input.clear()
        self.teacher_input.clear()
        self.course_title_input.clear()
        self.course_code_input.clear()
        self.classroom_input.clear()
        self.lecture_duration_input.clear()  # Clear lecture duration field
        self.start_time_input.setTime(QTime.currentTime())
        self.end_time_input.setTime(QTime.currentTime())
        self.session_combo.setCurrentIndex(0)

    def is_teacher_scheduled(self, teacher, start_time, end_time):
        query = """
        SELECT * FROM Timetable 
        WHERE teacher = ? AND 
              ((lecture_start_time < ? AND lecture_end_time > ?) OR 
               (lecture_start_time < ? AND lecture_end_time > ?))
        """
        self.cursor.execute(query, (teacher, end_time, start_time, start_time, end_time))
        return bool(self.cursor.fetchall())

def main():
    app = QApplication(sys.argv)
    window = CreateTimetableWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
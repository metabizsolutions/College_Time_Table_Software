import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QMessageBox, QTimeEdit
)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont

class LabWorkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Work")
        self.setGeometry(100, 100, 400, 500)  # Increased height to accommodate new fields

        # Connect to the database
        self.conn = sqlite3.connect('timetable.db')
        self.cursor = self.conn.cursor()

        # Create the LabWork table if it doesn't exist
        self.create_lab_work_table()

        # Main layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Department Selection
        self.department_label = QLabel("Select Department:")
        self.department_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.department_label)

        self.department_combo = QComboBox()
        self.populate_departments()  # Fetch departments from the Programs table
        self.layout.addWidget(self.department_combo)

        # Semester Selection
        self.semester_label = QLabel("Select Semester:")
        self.semester_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.semester_label)

        self.semester_combo = QComboBox()
        self.semester_combo.addItems(["1", "2", "3", "4", "5", "6", "7", "8"])  # Add semesters
        self.layout.addWidget(self.semester_combo)

        # Session Selection
        self.session_label = QLabel("Select Session:")
        self.session_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.session_label)

        self.session_combo = QComboBox()
        self.session_combo.addItems(["Morning", "Evening"])  # Add sessions
        self.layout.addWidget(self.session_combo)

        # Subject Selection
        self.subject_label = QLabel("Select Subject:")
        self.subject_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.subject_label)

        self.subject_combo = QComboBox()
        self.populate_subjects()  # Fetch subjects from the Courses table
        self.layout.addWidget(self.subject_combo)

        # Teacher Selection
        self.teacher_label = QLabel("Select Teacher:")
        self.teacher_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.teacher_label)

        self.teacher_combo = QComboBox()
        self.populate_teachers()  # Fetch teachers from the Teachers table
        self.layout.addWidget(self.teacher_combo)

        # Day Selection
        self.day_label = QLabel("Select Day:")
        self.day_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.day_label)

        self.day_combo = QComboBox()
        self.day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.layout.addWidget(self.day_combo)

        # Start Time Selection
        self.start_time_label = QLabel("Select Start Time:")
        self.start_time_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.start_time_label)

        self.start_time_input = QTimeEdit()
        self.start_time_input.setDisplayFormat("hh:mm AP")  # 12-hour format with AM/PM
        self.start_time_input.setTime(QTime.currentTime())
        self.layout.addWidget(self.start_time_input)

        # End Time Selection
        self.end_time_label = QLabel("Select End Time:")
        self.end_time_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.end_time_label)

        self.end_time_input = QTimeEdit()
        self.end_time_input.setDisplayFormat("hh:mm AP")  # 12-hour format with AM/PM
        self.end_time_input.setTime(QTime.currentTime())
        self.layout.addWidget(self.end_time_input)

        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_lab_work)
        self.layout.addWidget(self.submit_button)

    def create_lab_work_table(self):
        """Create the LabWork table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS LabWork (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            semester TEXT NOT NULL,
            session TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            teacher_name TEXT NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def populate_departments(self):
        """Fetch departments from the Programs table and populate the combo box."""
        query = "SELECT DISTINCT program_name FROM Programs"
        self.cursor.execute(query)
        departments = self.cursor.fetchall()
        for department in departments:
            self.department_combo.addItem(department[0])

    def populate_subjects(self):
        """Fetch subjects from the Courses table and populate the combo box."""
        query = "SELECT course_name FROM Courses"
        self.cursor.execute(query)
        subjects = self.cursor.fetchall()
        for subject in subjects:
            self.subject_combo.addItem(subject[0])

    def populate_teachers(self):
        """Fetch teachers from the Teachers table and populate the combo box."""
        query = "SELECT teacher_name FROM Teachers"
        self.cursor.execute(query)
        teachers = self.cursor.fetchall()
        for teacher in teachers:
            self.teacher_combo.addItem(teacher[0])

    def submit_lab_work(self):
        """Store the selected department, semester, session, subject, teacher, day, start time, and end time in the LabWork table."""
        department = self.department_combo.currentText()
        semester = self.semester_combo.currentText()
        session = self.session_combo.currentText()
        subject = self.subject_combo.currentText()
        teacher = self.teacher_combo.currentText()
        day = self.day_combo.currentText()
        start_time = self.start_time_input.time().toString("hh:mm AP")  # Format as 12-hour time
        end_time = self.end_time_input.time().toString("hh:mm AP")  # Format as 12-hour time

        if not department or not semester or not session or not subject or not teacher or not day or not start_time or not end_time:
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return

        try:
            query = """
            INSERT INTO LabWork (department, semester, session, subject_name, teacher_name, day, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (department, semester, session, subject, teacher, day, start_time, end_time))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Lab work data saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

    def closeEvent(self, event):
        """Close the database connection when the window is closed."""
        self.conn.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = LabWorkWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QComboBox, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from database import fetch_query_results  # Import the fetch_query_results function

class GenerateReportWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Create Timetable")
        self.setGeometry(100, 100, 800, 600)

        # Set up the layout for the window
        self.main_layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Generate Timetable Report")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Create a form layout for semester selection
        self.form_layout = QFormLayout()

        # Semester combo box
        self.semester_label = QLabel("Select Semester:")
        self.semester_combo = QComboBox()
        self.semester_combo.addItems(self.get_semesters())  # Fetch semesters from the database
        self.semester_combo.currentTextChanged.connect(self.update_department_table)  # Connect to update departments
        self.form_layout.addRow(self.semester_label, self.semester_combo)

        # Add form layout to main layout
        self.main_layout.addLayout(self.form_layout)

        # Button to show the timetable table
        self.generate_button = QPushButton("Show Timetable")
        self.generate_button.clicked.connect(self.show_timetable)
        self.main_layout.addWidget(self.generate_button)

        # Table for displaying timetable (initially hidden)
        self.timetable_table = QTableWidget(5, 10)  # 5 rows (departments), 10 columns (Department, Classroom, Lecture slots)
        self.timetable_table.setHorizontalHeaderLabels([
            "Department", "Classroom", "Lecture 1", "Lecture 2", 
            "Lecture 3", "Lecture 4", "Lecture 5", "Lecture 6", 
            "Lecture 7", "Lecture 8"
        ])
        self.timetable_table.setVerticalHeaderLabels([f"Dpt. {i+1}" for i in range(5)])  # Placeholder labels
        self.timetable_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make cells non-editable
        self.timetable_table.setAlternatingRowColors(True)  # Alternate row colors for readability

        # Set the cell height for each row
        row_height = 100  # Adjust the height as needed
        for row in range(5):  # For all rows
            self.timetable_table.setRowHeight(row, row_height)

        # Set the width for each column individually
        self.timetable_table.setColumnWidth(0, 200)  # Department column
        self.timetable_table.setColumnWidth(1, 80)  # Classroom column
        self.timetable_table.setColumnWidth(2, 120)  # Lecture 1
        self.timetable_table.setColumnWidth(3, 120)  # Lecture 2
        self.timetable_table.setColumnWidth(4, 120)  # Lecture 3
        self.timetable_table.setColumnWidth(5, 120)  # Lecture 4
        self.timetable_table.setColumnWidth(6, 120)  # Lecture 5
        self.timetable_table.setColumnWidth(7, 120)  # Lecture 6
        self.timetable_table.setColumnWidth(8, 120)  # Lecture 7
        self.timetable_table.setColumnWidth(9, 120)  # Lecture 8


        self.main_layout.addWidget(self.timetable_table)
        self.setLayout(self.main_layout)

    # Rest of the methods remain unchanged...



    def get_semesters(self):
        """Fetch all distinct semesters from the Programs table."""
        query = "SELECT DISTINCT semester FROM Programs"
        semesters = fetch_query_results(query)
        return [semester[0] for semester in semesters]

    def update_department_table(self):
        """Update the timetable table when a semester is selected."""
        semester = self.semester_combo.currentText()
        if semester:
            # Clear existing table data before updating
            self.timetable_table.clearContents()
            self.timetable_table.setRowCount(5)  # Reset row count if needed
            
            # Fetch departments, classrooms, and courses associated with the selected semester
            departments_data = self.get_departments_classrooms_and_courses_for_semester(semester)
            self.populate_table_with_departments_and_courses(departments_data)
        else:
            self.timetable_table.clearContents()  # Clear the table if no semester is selected

    def get_departments_classrooms_and_courses_for_semester(self, semester):
        """Fetch all departments, classrooms, courses, and their details for the selected semester."""
        query = """
            SELECT department, classroom, course_title, course_code, teacher, 
                   lecture_start_time, lecture_end_time
            FROM Timetable 
            WHERE semester = ?
        """
        return fetch_query_results(query, (semester,))

    def populate_table_with_departments_and_courses(self, departments_data):
        """Populate the table with departments, classrooms, and courses."""
        self.timetable_table.setRowCount(len(departments_data))  # Set row count based on number of departments

        department_counter = 0
        row_counter = 0
        lecture_headers = {}  # Dictionary to store lecture times for headers

        for i, (department, classroom, course_title, course_code, teacher, start_time, end_time) in enumerate(departments_data):
            # Set department and classroom details in the first two columns
            if department_counter == 0:
                self.timetable_table.setItem(row_counter, 0, QTableWidgetItem(department))
                self.timetable_table.setItem(row_counter, 1, QTableWidgetItem(classroom))

            # Dynamically populate the lecture headers (Start - End times) for each lecture
            lecture_info = f"{course_title} ({course_code}) {teacher}"
            time_slot = f"{start_time}-{end_time}"

            # Store time slot in lecture_headers if it's not already there
            if (start_time, end_time) not in lecture_headers:
                lecture_headers[len(lecture_headers) + 1] = (start_time, end_time)

            # Insert lecture info in the table cells (up to 8 slots)
            for j in range(2, 10):  # Columns for Lecture 1 to Lecture 8
                if not self.timetable_table.item(row_counter, j):
                    # Only insert lecture info in the first available (empty) cell in each row
                    if j - 2 < len(departments_data):  # Check if we have enough lectures for this column
                        # Populate the slot with lecture info only if there are enough lectures for it
                        self.timetable_table.setItem(row_counter, j, QTableWidgetItem(lecture_info))
                        break

            department_counter += 1

            # If there are more lectures, start a new row for the department
            if department_counter == 6:
                department_counter = 0
                row_counter += 1

        # Set dynamic column headers with the correct times (Start-End)
        lecture_column = 2
        for i, (start_time, end_time) in lecture_headers.items():
            time_slot_header = f"Lecture {i} ({start_time}-{end_time})"
            self.timetable_table.setHorizontalHeaderItem(lecture_column, QTableWidgetItem(time_slot_header))
            lecture_column += 1

        # Clear remaining columns for empty rows (empty cells for unused slots)
        for row in range(len(departments_data)):
            for col in range(2, 10):  # Columns for Lecture 1 to Lecture 8
                if not self.timetable_table.item(row, col):  # Check if the cell is empty
                    self.timetable_table.setItem(row, col, QTableWidgetItem(""))  # Empty for now




    def show_timetable(self):
        """Show the timetable after selecting a semester."""
        semester = self.semester_combo.currentText()

        if not semester:
            QMessageBox.warning(self, "Input Error", "Please select a semester.")
            return

        # Fetch timetable data for the selected semester
        department_data = self.get_departments_classrooms_and_courses_for_semester(semester)

        if not department_data:
            QMessageBox.warning(self, "No Data", "No departments found for the selected semester.")
            return

        # Populate the first column (Department) and second column (Classroom)
        self.populate_table_with_departments_and_courses(department_data)

        self.timetable_table.setVisible(True)  # Make the table visible after selection
        QMessageBox.information(self, "Success", f"Timetable for semester {semester} displayed.")

def main():
    app = QApplication(sys.argv)
    window = GenerateReportWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

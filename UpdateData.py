import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QListWidget, QTableWidget, QTableWidgetItem,
                             QLineEdit, QHBoxLayout, QMessageBox, QInputDialog, QApplication)
from PyQt5.QtCore import Qt
from database import fetch_query_results, execute_query  # Import your database functions


class UpdateDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Data")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.main_layout = QVBoxLayout(self)

        # Buttons for update actions
        self.update_classroom_button = QPushButton("Update Classroom")
        self.update_teacher_button = QPushButton("Update Teacher")
        self.update_courses_button = QPushButton("Update Courses")

        self.update_classroom_button.clicked.connect(self.show_classroom_search)
        self.update_teacher_button.clicked.connect(self.show_teacher_search)
        self.update_courses_button.clicked.connect(self.show_courses_search)

        # Add buttons to the layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_classroom_button)
        button_layout.addWidget(self.update_teacher_button)
        button_layout.addWidget(self.update_courses_button)

        self.main_layout.addLayout(button_layout)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_results)

        self.main_layout.addWidget(self.search_bar)

        # List widget for displaying classroom results (single column)
        self.result_list = QListWidget()

        # Table widget for displaying teacher and course results (multiple columns)
        self.result_table = QTableWidget()

        self.main_layout.addWidget(self.result_list)  # Initially add the list for classrooms
        self.main_layout.addWidget(self.result_table)  # Add the table for teachers and courses

        # Set the layout
        self.setLayout(self.main_layout)

        # Initially hide the search bar, result list, and result table
        self.search_bar.setVisible(False)
        self.result_list.setVisible(False)
        self.result_table.setVisible(False)

    def show_classroom_search(self):
        # Show list widget for classroom updates
        self.search_bar.setVisible(True)
        self.result_list.setVisible(True)
        self.result_table.setVisible(False)  # Hide the table
        self.search_bar.clear()
        self.result_list.clear()
        self.result_list.itemClicked.connect(self.classroom_item_clicked)
        self.fetch_classroom_data()  # Fetch initial classroom data

    def show_teacher_search(self):
        # Show table widget for teacher updates
        self.search_bar.setVisible(True)
        self.result_list.setVisible(False)  # Hide the list
        self.result_table.setVisible(True)
        self.search_bar.clear()
        self.result_table.clear()
        self.fetch_teacher_data()  # Fetch initial teacher data

    def show_courses_search(self):
        # Show table widget for course updates
        self.search_bar.setVisible(True)
        self.result_list.setVisible(False)  # Hide the list
        self.result_table.setVisible(True)
        self.search_bar.clear()
        self.result_table.clear()
        self.fetch_course_data()  # Fetch initial course data

    def filter_results(self):
        search_text = self.search_bar.text().lower()
        if self.update_classroom_button.isChecked():
            self.fetch_classroom_data(search_text)
        elif self.update_teacher_button.isChecked():
            self.fetch_teacher_data(search_text)
        elif self.update_courses_button.isChecked():
            self.fetch_course_data(search_text)

    def fetch_classroom_data(self, search_text=""):
        """Fetch classroom names from the database based on the search query."""
        query = "SELECT classroom_id, classroom_name FROM Classrooms WHERE LOWER(classroom_name) LIKE ?"
        search_pattern = f"%{search_text}%"  # SQL pattern for matching
        results = fetch_query_results(query, (search_pattern,))

        self.result_list.clear()
        if results:
            for classroom in results:
                item = QListWidgetItem(classroom[1])  # Display only classroom name
                item.setData(Qt.UserRole, classroom[0])  # Store ID
                self.result_list.addItem(item)
        else:
            self.result_list.addItem("No classrooms found.")

    def fetch_teacher_data(self, search_text=""):
        """Fetch teacher data from the database based on the search query."""
        query = "SELECT teacher_id, teacher_name, bps_grade, specialization FROM Teachers WHERE LOWER(teacher_name) LIKE ?"
        search_pattern = f"%{search_text}%"
        results = fetch_query_results(query, (search_pattern,))

        # Set up table with 3 columns for teacher data
        self.result_table.setRowCount(len(results))
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Teacher Name", "BPS Grade", "Specialization"])

        if results:
            for row_num, teacher in enumerate(results):
                self.result_table.setItem(row_num, 0, QTableWidgetItem(teacher[1]))
                self.result_table.setItem(row_num, 1, QTableWidgetItem(str(teacher[2])))
                self.result_table.setItem(row_num, 2, QTableWidgetItem(teacher[3]))
                self.result_table.setRowHeight(row_num, 25)  # Set row height
        else:
            self.result_table.setRowCount(0)
            QMessageBox.information(self, "No Teachers", "No teachers found.")

    def fetch_course_data(self, search_text=""):
        """Fetch course data from the database based on the search query."""
        query = "SELECT course_id, course_name, course_code, credits FROM Courses WHERE LOWER(course_name) LIKE ?"
        search_pattern = f"%{search_text}%"
        results = fetch_query_results(query, (search_pattern,))

        # Set up table with 3 columns for course data
        self.result_table.setRowCount(len(results))
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Course Name", "Course Code", "Credits"])

        if results:
            for row_num, course in enumerate(results):
                self.result_table.setItem(row_num, 0, QTableWidgetItem(course[1]))
                self.result_table.setItem(row_num, 1, QTableWidgetItem(course[2]))
                self.result_table.setItem(row_num, 2, QTableWidgetItem(str(course[3])))
                self.result_table.setRowHeight(row_num, 25)  # Set row height
        else:
            self.result_table.setRowCount(0)
            QMessageBox.information(self, "No Courses", "No courses found.")

    def classroom_item_clicked(self, item):
        """Handle classroom item selection."""
        classroom_id = item.data(Qt.UserRole)
        self.update_classroom(classroom_id)

    def update_classroom(self, classroom_id):
        """Update classroom name."""
        current_name = self.result_list.currentItem().text()
        new_name, ok = QInputDialog.getText(self, "Update Classroom", "Enter new classroom name:", text=current_name)
        if ok and new_name:
            query = "UPDATE Classrooms SET classroom_name = ? WHERE classroom_id = ?"
            execute_query(query, (new_name, classroom_id))
            QMessageBox.information(self, "Success", "Classroom updated successfully!")
            self.fetch_classroom_data()  # Refresh list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateDataWindow()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QListWidget,
                             QLineEdit, QHBoxLayout, QMessageBox, QInputDialog, QApplication, QListWidgetItem)
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

        # List widget for displaying results
        self.result_list = QListWidget()
        self.main_layout.addWidget(self.result_list)

        # Set the layout
        self.setLayout(self.main_layout)

        # Initially hide the search bar and result list
        self.search_bar.setVisible(False)
        self.result_list.setVisible(False)

    def show_classroom_search(self):
        self.search_bar.setVisible(True)
        self.result_list.setVisible(True)
        self.search_bar.clear()
        self.result_list.clear()
        self.result_list.itemClicked.connect(self.classroom_item_clicked)

    def show_teacher_search(self):
        self.search_bar.setVisible(True)
        self.result_list.setVisible(True)
        self.search_bar.clear()
        self.result_list.clear()
        self.result_list.itemClicked.connect(self.teacher_item_clicked)
        self.fetch_teacher_data()  # Fetch initial teacher data

    def show_courses_search(self):
        self.search_bar.setVisible(True)
        self.result_list.setVisible(True)
        self.search_bar.clear()
        self.result_list.clear()
        self.result_list.itemClicked.connect(self.course_item_clicked)
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

        self.result_list.clear()
        if results:
            for teacher in results:
                item = QListWidgetItem(f"{teacher[1]} - {teacher[2]} - {teacher[3]}")  # Display name, grade, specialization
                item.setData(Qt.UserRole, teacher[0])  # Store teacher ID
                self.result_list.addItem(item)
        else:
            self.result_list.addItem("No teachers found.")

    def fetch_course_data(self, search_text=""):
        """Fetch course data from the database based on the search query."""
        query = "SELECT course_id, course_name, course_code, credits FROM Courses WHERE LOWER(course_name) LIKE ?"
        search_pattern = f"%{search_text}%"
        results = fetch_query_results(query, (search_pattern,))

        self.result_list.clear()
        if results:
            for course in results:
                item = QListWidgetItem(f"{course[1]} - {course[2]} - {course[3]}")  # Display course details
                item.setData(Qt.UserRole, course[0])  # Store course ID
                self.result_list.addItem(item)
        else:
            self.result_list.addItem("No courses found.")

    def classroom_item_clicked(self, item):
        """Handle classroom item selection."""
        classroom_id = item.data(Qt.UserRole)
        self.update_classroom(classroom_id)

    def teacher_item_clicked(self, item):
        """Handle teacher item selection."""
        teacher_id = item.data(Qt.UserRole)
        self.update_teacher(teacher_id)

    def course_item_clicked(self, item):
        """Handle course item selection."""
        course_id = item.data(Qt.UserRole)
        self.update_course(course_id)

    def update_classroom(self, classroom_id):
        """Update classroom name."""
        current_name = self.result_list.currentItem().text()
        new_name, ok = QInputDialog.getText(self, "Update Classroom", "Enter new classroom name:", text=current_name)
        if ok and new_name:
            query = "UPDATE Classrooms SET classroom_name = ? WHERE classroom_id = ?"
            execute_query(query, (new_name, classroom_id))
            QMessageBox.information(self, "Success", "Classroom updated successfully!")
            self.fetch_classroom_data()  # Refresh list

    def update_teacher(self, teacher_id):
        """Update teacher data."""
        current_info = self.result_list.currentItem().text().split(" - ")
        new_name, ok1 = QInputDialog.getText(self, "Update Teacher Name", "Enter new teacher name:", text=current_info[0])
        new_grade, ok2 = QInputDialog.getText(self, "Update BPS Grade", "Enter new BPS grade:", text=current_info[1])
        new_specialization, ok3 = QInputDialog.getText(self, "Update Specialization", "Enter new specialization:", text=current_info[2])
        
        if ok1 and new_name and ok2 and new_grade and ok3 and new_specialization:
            query = "UPDATE Teachers SET teacher_name = ?, bps_grade = ?, specialization = ? WHERE teacher_id = ?"
            execute_query(query, (new_name, new_grade, new_specialization, teacher_id))
            QMessageBox.information(self, "Success", "Teacher updated successfully!")
            self.fetch_teacher_data()  # Refresh list

    def update_course(self, course_id):
        """Update course data."""
        current_info = self.result_list.currentItem().text().split(" - ")
        new_name, ok1 = QInputDialog.getText(self, "Update Course Name", "Enter new course name:", text=current_info[0])
        new_code, ok2 = QInputDialog.getText(self, "Update Course Code", "Enter new course code:", text=current_info[1])
        new_credits, ok3 = QInputDialog.getText(self, "Update Credits", "Enter new credits:", text=current_info[2])
        
        if ok1 and new_name and ok2 and new_code and ok3 and new_credits:
            query = "UPDATE Courses SET course_name = ?, course_code = ?, credits = ? WHERE course_id = ?"
            execute_query(query, (new_name, new_code, new_credits, course_id))
            QMessageBox.information(self, "Success", "Course updated successfully!")
            self.fetch_course_data()  # Refresh list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateDataWindow()
    window.show()
    sys.exit(app.exec_())

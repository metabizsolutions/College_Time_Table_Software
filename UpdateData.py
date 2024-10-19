import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableView, QMessageBox, QHBoxLayout, QInputDialog, QHeaderView
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import sqlite3


class UpdateDataWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Update Classrooms')
        self.setGeometry(100, 100, 600, 400)

        # Layouts
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        # Search bar to enter the classroom name
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter classroom name to search...")
        search_layout.addWidget(self.search_bar)

        # Search button
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_classroom)
        search_layout.addWidget(self.search_btn)

        # Add the search layout to the main layout
        main_layout.addLayout(search_layout)

        # Table view to display the search results
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table_view)

        # Set the main layout for the window
        self.setLayout(main_layout)

        # Initialize SQLite connection
        self.conn = sqlite3.connect('timetable.db')
        self.cur = self.conn.cursor()

        # Store selected classroom ID
        self.selected_classroom_id = None

        # Update and Delete buttons
        self.update_button = QPushButton("Update Selected")
        self.update_button.clicked.connect(self.update_classroom)
        self.update_button.setEnabled(False)
        main_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_classroom)
        self.delete_button.setEnabled(False)
        main_layout.addWidget(self.delete_button)

    def search_classroom(self):
        """Search for classrooms based on the search bar input."""
        search_query = self.search_bar.text()

        if search_query:
            query = "SELECT * FROM Classrooms WHERE classroom_name LIKE ?"
            search_pattern = f'%{search_query}%'
            self.cur.execute(query, (search_pattern,))
        else:
            query = "SELECT * FROM Classrooms"  # Fetch all records if search is empty
            self.cur.execute(query)

        results = self.cur.fetchall()

        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No results", "No classroom found with that name.")

    def display_results(self, results):
        """Display the search results in the classroom table."""
        headers = ['Classroom ID', 'Classroom Name']

        model = QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row, data in enumerate(results):
            for column, value in enumerate(data):
                item = QStandardItem(str(value))
                model.setItem(row, column, item)

        self.table_view.setModel(model)

        self.table_view.clicked.connect(self.table_item_clicked)

    def table_item_clicked(self, index):
        """Handle the table item click event."""
        self.selected_classroom_id = int(self.table_view.model().item(index.row(), 0).text())
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def update_classroom(self):
        """Update the selected classroom."""
        if self.selected_classroom_id is not None:
            current_data_query = "SELECT * FROM Classrooms WHERE classroom_id = ?"
            self.cur.execute(current_data_query, (self.selected_classroom_id,))
            current_data = self.cur.fetchone()

            if current_data is None:
                QMessageBox.warning(self, "Error", "Classroom not found!")
                return

            new_name, ok_name = QInputDialog.getText(self, "Update Classroom Name",
                                                     f"Current name: {current_data[1]}\nEnter new name:")

            if ok_name and new_name:
                update_query = "UPDATE Classrooms SET classroom_name = ? WHERE classroom_id = ?"
                self.cur.execute(update_query, (new_name, self.selected_classroom_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Classroom updated successfully!")
                self.search_classroom()  # Refresh the table view with updated data

    def delete_classroom(self):
        """Delete the selected classroom."""
        if self.selected_classroom_id is not None:
            confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this classroom?")
            if confirm == QMessageBox.Yes:
                delete_query = "DELETE FROM Classrooms WHERE classroom_id = ?"
                self.cur.execute(delete_query, (self.selected_classroom_id,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Classroom deleted successfully!")
                self.search_classroom()  # Refresh the table view


class UpdateTeachersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Update Teachers')
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter teacher name to search...")
        search_layout.addWidget(self.search_bar)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_teacher)
        search_layout.addWidget(self.search_btn)

        main_layout.addLayout(search_layout)

        self.table_view = QTableView()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table_view)

        self.setLayout(main_layout)

        self.conn = sqlite3.connect('timetable.db')
        self.cur = self.conn.cursor()

        self.selected_teacher_id = None

        self.update_button = QPushButton("Update Selected")
        self.update_button.clicked.connect(self.update_teacher)
        self.update_button.setEnabled(False)
        main_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_teacher)
        self.delete_button.setEnabled(False)
        main_layout.addWidget(self.delete_button)

    def search_teacher(self):
        search_query = self.search_bar.text()

        if search_query:
            query = "SELECT * FROM Teachers WHERE teacher_name LIKE ?"
            search_pattern = f'%{search_query}%'
            self.cur.execute(query, (search_pattern,))
        else:
            query = "SELECT * FROM Teachers"
            self.cur.execute(query)

        results = self.cur.fetchall()

        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No results", "No teacher found with that name.")

    def display_results(self, results):
        headers = ['Teacher ID', 'Name', 'BPS Grade', 'Specialization']

        model = QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row, data in enumerate(results):
            for column, value in enumerate(data):
                item = QStandardItem(str(value))
                model.setItem(row, column, item)

        self.table_view.setModel(model)

        self.table_view.clicked.connect(self.table_item_clicked)

    def table_item_clicked(self, index):
        self.selected_teacher_id = int(self.table_view.model().item(index.row(), 0).text())
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def update_teacher(self):
        if self.selected_teacher_id is not None:
            current_data_query = "SELECT * FROM Teachers WHERE teacher_id = ?"
            self.cur.execute(current_data_query, (self.selected_teacher_id,))
            current_data = self.cur.fetchone()

            if current_data is None:
                QMessageBox.warning(self, "Error", "Teacher not found!")
                return

            new_name, ok_name = QInputDialog.getText(self, "Update Teacher Name",
                                                     f"Current name: {current_data[1]}\nEnter new name:")
            new_grade, ok_grade = QInputDialog.getText(self, "Update Teacher Grade",
                                                       f"Current grade: {current_data[2]}\nEnter new grade:")
            new_specialization, ok_spec = QInputDialog.getText(self, "Update Teacher Specialization",
                                                               f"Current specialization: {current_data[3]}\nEnter new specialization:")

            if ok_name and new_name and ok_grade and new_grade and ok_spec and new_specialization:
                update_query = "UPDATE Teachers SET teacher_name = ?, bps_grade = ?, specialization = ? WHERE teacher_id = ?"
                self.cur.execute(update_query, (new_name, new_grade, new_specialization, self.selected_teacher_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Teacher updated successfully!")
                self.search_teacher()

    def delete_teacher(self):
        if self.selected_teacher_id is not None:
            confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this teacher?")
            if confirm == QMessageBox.Yes:
                delete_query = "DELETE FROM Teachers WHERE teacher_id = ?"
                self.cur.execute(delete_query, (self.selected_teacher_id,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Teacher deleted successfully!")
                self.search_teacher()


class UpdateCoursesWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Update Courses')
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter course name to search...")
        search_layout.addWidget(self.search_bar)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_course)
        search_layout.addWidget(self.search_btn)

        main_layout.addLayout(search_layout)

        self.table_view = QTableView()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table_view)

        self.setLayout(main_layout)

        self.conn = sqlite3.connect('timetable.db')
        self.cur = self.conn.cursor()

        self.selected_course_id = None

        self.update_button = QPushButton("Update Selected")
        self.update_button.clicked.connect(self.update_course)
        self.update_button.setEnabled(False)
        main_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_course)
        self.delete_button.setEnabled(False)
        main_layout.addWidget(self.delete_button)

    def search_course(self):
        search_query = self.search_bar.text()

        if search_query:
            query = "SELECT * FROM Courses WHERE course_name LIKE ?"
            search_pattern = f'%{search_query}%'
            self.cur.execute(query, (search_pattern,))
        else:
            query = "SELECT * FROM Courses"
            self.cur.execute(query)

        results = self.cur.fetchall()

        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No results", "No course found with that name.")

    def display_results(self, results):
        headers = ['Course ID', 'Name', 'Course Code', 'Credits']

        model = QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row, data in enumerate(results):
            for column, value in enumerate(data):
                item = QStandardItem(str(value))
                model.setItem(row, column, item)

        self.table_view.setModel(model)

        self.table_view.clicked.connect(self.table_item_clicked)

    def table_item_clicked(self, index):
        self.selected_course_id = int(self.table_view.model().item(index.row(), 0).text())
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def update_course(self):
        if self.selected_course_id is not None:
            current_data_query = "SELECT * FROM Courses WHERE course_id = ?"
            self.cur.execute(current_data_query, (self.selected_course_id,))
            current_data = self.cur.fetchone()

            if current_data is None:
                QMessageBox.warning(self, "Error", "Course not found!")
                return

            new_name, ok_name = QInputDialog.getText(self, "Update Course Name",
                                                     f"Current name: {current_data[1]}\nEnter new name:")
            new_code, ok_code = QInputDialog.getText(self, "Update Course Code",
                                                     f"Current code: {current_data[2]}\nEnter new code:")
            new_credits, ok_credits = QInputDialog.getText(self, "Update Course Credits",
                                                           f"Current credits: {current_data[3]}\nEnter new credits:")

            if ok_name and new_name and ok_code and new_code and ok_credits and new_credits:
                update_query = "UPDATE Courses SET course_name = ?, course_code = ?, credits = ? WHERE course_id = ?"
                self.cur.execute(update_query, (new_name, new_code, new_credits, self.selected_course_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Course updated successfully!")
                self.search_course()

    def delete_course(self):
        if self.selected_course_id is not None:
            confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this course?")
            if confirm == QMessageBox.Yes:
                delete_query = "DELETE FROM Courses WHERE course_id = ?"
                self.cur.execute(delete_query, (self.selected_course_id,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Course deleted successfully!")
                self.search_course()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Update Records')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        btn_update_classrooms = QPushButton("Update Classrooms")
        btn_update_classrooms.clicked.connect(self.show_update_classrooms_window)
        layout.addWidget(btn_update_classrooms)

        btn_update_teachers = QPushButton("Update Teachers")
        btn_update_teachers.clicked.connect(self.show_update_teachers_window)
        layout.addWidget(btn_update_teachers)

        btn_update_courses = QPushButton("Update Courses")
        btn_update_courses.clicked.connect(self.show_update_courses_window)
        layout.addWidget(btn_update_courses)

        self.setLayout(layout)

    def show_update_classrooms_window(self):
        self.update_classrooms_window = UpdateDataWindow()
        self.update_classrooms_window.show()

    def show_update_teachers_window(self):
        self.update_teachers_window = UpdateTeachersWindow()
        self.update_teachers_window.show()

    def show_update_courses_window(self):
        self.update_courses_window = UpdateCoursesWindow()
        self.update_courses_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

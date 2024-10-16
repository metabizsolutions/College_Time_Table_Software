import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, 
    QListWidget, QMessageBox, QHBoxLayout, QInputDialog, 
    QTableView, QHeaderView
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import sqlite3


class UpdateDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Classrooms")
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        self.layout = QVBoxLayout()

        # Update Classroom Button
        self.update_classroom_button = QPushButton("Update Classrooms")
        self.update_classroom_button.clicked.connect(self.show_search_bar)
        self.layout.addWidget(self.update_classroom_button)

        # Search Bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search classrooms...")
        self.search_bar.textChanged.connect(self.search_classrooms)
        self.layout.addWidget(self.search_bar)

        # Classroom List
        self.classroom_list = QListWidget()
        self.classroom_list.itemClicked.connect(self.classroom_item_clicked)
        self.layout.addWidget(self.classroom_list)

        # Update and Delete buttons
        self.update_button = QPushButton("Update Selected")
        self.update_button.clicked.connect(self.update_classroom)
        self.update_button.setVisible(False)
        self.layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_classroom)
        self.delete_button.setVisible(False)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

        # Database connection
        self.connection = sqlite3.connect('timetable.db')  # Modify with your actual database path
        self.cursor = self.connection.cursor()

        # Store selected classroom ID and name
        self.selected_classroom_id = None
        self.selected_classroom_name = None

    def show_search_bar(self):
        """Display the search bar and initialize the list."""
        self.search_bar.setVisible(True)
        self.classroom_list.setVisible(True)
        self.search_classrooms()

    def search_classrooms(self):
        """Search for classrooms based on the search bar input."""
        search_text = self.search_bar.text()
        query = "SELECT classroom_id, classroom_name FROM Classrooms WHERE classroom_name LIKE ?"
        search_pattern = f'%{search_text}%'
        self.cursor.execute(query, (search_pattern,))
        results = self.cursor.fetchall()

        self.classroom_list.clear()
        for classroom in results:
            item = QListWidgetItem(classroom[1])  # Display classroom name
            item.setData(1, classroom[0])  # Store classroom ID
            self.classroom_list.addItem(item)

    def classroom_item_clicked(self, item):
        """Handle the classroom list item click event."""
        self.selected_classroom_id = item.data(1)  # Get selected classroom ID
        self.selected_classroom_name = item.text()  # Get selected classroom name
        self.update_button.setVisible(True)
        self.delete_button.setVisible(True)

    def update_classroom(self):
        """Update the selected classroom by fetching its current data."""
        if self.selected_classroom_id is not None:
            # Display the current classroom name in the input dialog for editing
            new_name, ok = QInputDialog.getText(self, "Update Classroom", 
                                                f"Current name: {self.selected_classroom_name}\nEnter new classroom name:")
            if ok and new_name:
                query = "UPDATE Classrooms SET classroom_name = ? WHERE classroom_id = ?"
                self.cursor.execute(query, (new_name, self.selected_classroom_id))
                self.connection.commit()
                QMessageBox.information(self, "Success", "Classroom updated successfully!")
                self.search_classrooms()  # Refresh the list with updated data

    def delete_classroom(self):
        """Delete the selected classroom."""
        if self.selected_classroom_id is not None:
            confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this classroom?")
            if confirm == QMessageBox.Yes:
                query = "DELETE FROM Classrooms WHERE classroom_id = ?"
                self.cursor.execute(query, (self.selected_classroom_id,))
                self.connection.commit()
                QMessageBox.information(self, "Success", "Classroom deleted successfully!")
                self.search_classrooms()  # Refresh the list


class UpdateTeachersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Update Teachers')
        self.setGeometry(100, 100, 600, 400)

        # Layouts
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        # Search bar to enter the teacher's name
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter teacher name to search...")
        search_layout.addWidget(self.search_bar)

        # Search button
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_teacher)
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
        self.conn = sqlite3.connect('timetable.db')  # Ensure your database path is correct
        self.cur = self.conn.cursor()

        # Store selected teacher ID
        self.selected_teacher_id = None

        # Update and Delete buttons
        self.update_button = QPushButton("Update Selected")
        self.update_button.clicked.connect(self.update_teacher)
        self.update_button.setEnabled(False)
        main_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_teacher)
        self.delete_button.setEnabled(False)
        main_layout.addWidget(self.delete_button)

    def search_teacher(self):
        """Search for teachers based on the search bar input."""
        search_query = self.search_bar.text()

        if search_query:
            query = f"SELECT * FROM Teachers WHERE teacher_name LIKE ?"
            search_pattern = f'%{search_query}%'
            self.cur.execute(query, (search_pattern,))
        else:
            query = "SELECT * FROM Teachers"  # Fetch all records if search is empty
            self.cur.execute(query)

        # Execute the query and fetch results
        results = self.cur.fetchall()

        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No results", "No teacher found with that name.")

    def display_results(self, results):
        """Display the search results in the teacher table."""
        # Define headers based on your "Teachers" table structure
        headers = ['Teacher ID', 'Name', 'BPS Grade', 'Specialization']

        # Populate the QTableView with the fetched data
        model = QStandardItemModel(len(results), len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row, data in enumerate(results):
            for column, value in enumerate(data):
                item = QStandardItem(str(value))
                model.setItem(row, column, item)

        self.table_view.setModel(model)

        # Enable update and delete buttons if a teacher is selected
        self.table_view.clicked.connect(self.table_item_clicked)

    def table_item_clicked(self, index):
        """Handle the table item click event."""
        self.selected_teacher_id = int(self.table_view.model().item(index.row(), 0).text())  # Get selected teacher ID
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def update_teacher(self):
        """Update the selected teacher by fetching its current data."""
        if self.selected_teacher_id is not None:
            current_data_query = "SELECT * FROM Teachers WHERE teacher_id = ?"
            self.cur.execute(current_data_query, (self.selected_teacher_id,))
            current_data = self.cur.fetchone()

            # Check if current_data is None
            if current_data is None:
                QMessageBox.warning(self, "Error", "Teacher not found!")
                return

            # Display the current teacher details in the input dialogs for editing
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
                self.search_teacher()  # Refresh the table view with updated data

    def delete_teacher(self):
        """Delete the selected teacher."""
        if self.selected_teacher_id is not None:
            confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this teacher?")
            if confirm == QMessageBox.Yes:
                delete_query = "DELETE FROM Teachers WHERE teacher_id = ?"
                self.cur.execute(delete_query, (self.selected_teacher_id,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Teacher deleted successfully!")
                self.search_teacher()  # Refresh the table view


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateTeachersWindow()
    window.show()
    sys.exit(app.exec_())

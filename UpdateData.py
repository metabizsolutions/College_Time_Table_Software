import sys
from PyQt5.QtWidgets import (QWidget, QListWidget, QListWidgetItem, QMessageBox, QInputDialog, QApplication, QLineEdit, QVBoxLayout, QMenu)
from PyQt5.QtCore import Qt
from database import fetch_query_results, execute_query  # Import your database functions


class UpdateDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Classrooms")
        self.setGeometry(100, 100, 600, 400)

        # Main layout that contains the search bar and classroom list
        self.main_layout = QVBoxLayout(self)

        # Add the search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Classrooms...")
        self.search_bar.textChanged.connect(self.filter_classrooms)
        self.main_layout.addWidget(self.search_bar)

        # Create a QListWidget for displaying the classrooms
        self.classroom_list = QListWidget(self)
        self.main_layout.addWidget(self.classroom_list)

        # Set the layout
        self.setLayout(self.main_layout)

        # Initialize the classroom list
        self.classroom_labels = []

    def filter_classrooms(self):
        """Fetch classroom names from the database based on the search query."""
        search_text = self.search_bar.text().lower()

        # Only proceed if there is a search query
        if search_text.strip():
            try:
                # Query to fetch matching classrooms from the 'Classrooms' table
                query = "SELECT classroom_id, classroom_name FROM Classrooms WHERE LOWER(classroom_name) LIKE ?"
                search_pattern = f"%{search_text}%"  # SQL pattern for matching
                results = fetch_query_results(query, (search_pattern,))  # Fetch filtered results

                # Clear the QListWidget before adding new results
                self.classroom_list.clear()

                if results:
                    # Iterate over the fetched results and create items for each classroom
                    for classroom in results:
                        classroom_id = classroom[0]
                        classroom_name = classroom[1]

                        # Create a list item for each classroom
                        item = QListWidgetItem(classroom_name)
                        item.setData(Qt.UserRole, classroom_id)  # Store the classroom ID in the item's data

                        # Add the item to the QListWidget
                        self.classroom_list.addItem(item)

                    # Connect item double-click to open the context menu
                    self.classroom_list.itemDoubleClicked.connect(self.on_double_click)

                else:
                    self.classroom_list.addItem("No classrooms found.")  # In case no data is found

            except Exception as e:
                self.classroom_list.addItem(f"Error fetching classrooms: {e}")  # Display error if any

    def on_double_click(self, item):
        """Handle double-click event to show the context menu."""
        self.show_context_menu(item)

    def show_context_menu(self, item):
        """Show a context menu with 'Update' and 'Delete' options."""
        classroom_id = item.data(Qt.UserRole)  # Get the classroom ID from the item's data

        menu = QMenu(self)
        update_action = menu.addAction("Update")
        delete_action = menu.addAction("Delete")

        action = menu.exec_(self.mapToGlobal(self.classroom_list.viewport().mapFromGlobal(QCursor.pos())))

        if action == update_action:
            self.update_classroom(item)
        elif action == delete_action:
            self.delete_classroom(item)

    def update_classroom(self, item):
        """Open a dialog to update the selected classroom."""
        classroom_id = item.data(Qt.UserRole)  # Get the classroom ID from the item's data
        current_name = item.text()

        # Prompt the user to enter a new classroom name
        new_name, ok = QInputDialog.getText(self, "Update Classroom", "Enter new classroom name:", text=current_name)

        if ok and new_name:
            try:
                # Update the classroom name in the database
                update_query = "UPDATE Classrooms SET classroom_name = ? WHERE classroom_id = ?"
                execute_query(update_query, (new_name, classroom_id))

                # Update the list item text to reflect the new name
                item.setText(new_name)
                QMessageBox.information(self, "Success", "Classroom updated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update classroom: {e}")

    def delete_classroom(self, item):
        """Delete the selected classroom from the database."""
        classroom_id = item.data(Qt.UserRole)  # Get the classroom ID from the item's data
        classroom_name = item.text()

        reply = QMessageBox.question(self, 'Delete Confirmation', f"Are you sure you want to delete classroom '{classroom_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # Perform the delete operation
                delete_query = "DELETE FROM Classrooms WHERE classroom_id = ?"
                execute_query(delete_query, (classroom_id,))
                QMessageBox.information(self, "Success", "Classroom deleted successfully.")

                # Remove the item from the list
                self.classroom_list.takeItem(self.classroom_list.row(item))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete classroom: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateDataWindow()
    window.show()
    sys.exit(app.exec_())

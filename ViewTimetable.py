import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, 
                             QLabel, QMessageBox, QApplication, 
                             QFormLayout, QLineEdit)  # Added QFormLayout and QLineEdit imports
from database import fetch_query_results, delete_record, update_record  # Importing necessary functions from the database module

class ViewTimetableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Timetable")
        self.setGeometry(100, 100, 800, 400)
        self.layout = QVBoxLayout(self)

        # Create a label for debugging to confirm file connection
        self.debug_label = QLabel("Loading timetable data...", self)
        self.layout.addWidget(self.debug_label)

        # Create the table widget to display the timetable
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        # Load the timetable data from the database
        self.load_timetable_data()

    def load_timetable_data(self):
        try:
            query = "SELECT * FROM Timetable"  # Modify this query according to your timetable table structure
            results = fetch_query_results(query)

            if results:
                self.debug_label.setText("Timetable data loaded successfully!")

                # Assuming `results` is a list of tuples, set up the table
                self.table_widget.setRowCount(len(results))
                self.table_widget.setColumnCount(len(results[0]) + 2)  # Adding space for buttons

                # Set table headers (adjust according to your table's columns)
                self.table_widget.setHorizontalHeaderLabels(['Lecture No', 'Department', 'Semester', 'Teacher', 
                                                              'Course Title', 'Course Code', 'Classroom', 
                                                              'Time', 'Session', 'Update', 'Delete'])

                # Populate the table with data and buttons
                for row_index, row_data in enumerate(results):
                    for col_index, data in enumerate(row_data):
                        self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

                    # Create Update button
                    update_button = QPushButton("Update")
                    update_button.clicked.connect(lambda checked, id=row_data[0]: self.open_update_window(id, row_data))
                    self.table_widget.setCellWidget(row_index, len(row_data), update_button)  # Last column for Update button

                    # Create Delete button
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda checked, id=row_data[0]: self.delete_record(id))
                    self.table_widget.setCellWidget(row_index, len(row_data) + 1, delete_button)  # Second last column for Delete button

            else:
                self.debug_label.setText("No timetable data available.")
                print("No data found in the timetable.")

        except Exception as e:
            self.debug_label.setText(f"Error loading timetable: {e}")
            print(f"Error loading timetable: {e}")

    def open_update_window(self, record_id, row_data):
        """Open the update window for the selected record."""
        self.update_window = UpdateTimetableWindow(record_id, row_data, self)
        self.update_window.show()

    def delete_record(self, record_id):
        """Delete a record from the timetable."""
        reply = QMessageBox.question(self, 'Delete Confirmation', f"Are you sure you want to delete record ID {record_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_record(record_id, "Timetable")
            self.load_timetable_data()  # Reload the data to reflect changes

class UpdateTimetableWindow(QWidget):
    def __init__(self, record_id, row_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Timetable Record")
        self.setGeometry(150, 150, 400, 300)

        self.record_id = record_id  # ID of the record to update
        self.row_data = row_data  # Current data of the record

        self.layout = QFormLayout(self)

        # Create input fields for each column in the timetable
        self.department_input = QLineEdit(self)
        self.department_input.setText(row_data[1])  # Assuming the second column is 'Department'
        self.layout.addRow("Department:", self.department_input)

        self.semester_input = QLineEdit(self)
        self.semester_input.setText(row_data[2])  # Assuming the third column is 'Semester'
        self.layout.addRow("Semester:", self.semester_input)

        self.teacher_input = QLineEdit(self)
        self.teacher_input.setText(row_data[3])  # Assuming the fourth column is 'Teacher'
        self.layout.addRow("Teacher:", self.teacher_input)

        self.course_title_input = QLineEdit(self)
        self.course_title_input.setText(row_data[4])  # Assuming the fifth column is 'Course Title'
        self.layout.addRow("Course Title:", self.course_title_input)

        self.course_code_input = QLineEdit(self)
        self.course_code_input.setText(row_data[5])  # Assuming the sixth column is 'Course Code'
        self.layout.addRow("Course Code:", self.course_code_input)

        self.classroom_input = QLineEdit(self)
        self.classroom_input.setText(row_data[6])  # Assuming the seventh column is 'Classroom'
        self.layout.addRow("Classroom:", self.classroom_input)

        self.time_input = QLineEdit(self)
        self.time_input.setText(row_data[7])  # Assuming the eighth column is 'Time'
        self.layout.addRow("Time:", self.time_input)

        self.session_input = QLineEdit(self)
        self.session_input.setText(row_data[8])  # Assuming the ninth column is 'Session'
        self.layout.addRow("Session:", self.session_input)

        # Create Update button
        self.update_button = QPushButton("Update", self)
        self.update_button.clicked.connect(self.update_record)
        self.layout.addRow(self.update_button)

        self.setLayout(self.layout)

    def update_record(self):
        """Update the record in the timetable with the new values."""
        updated_data = (
            self.department_input.text(),
            self.semester_input.text(),
            self.teacher_input.text(),
            self.course_title_input.text(),
            self.course_code_input.text(),
            self.classroom_input.text(),
            self.time_input.text(),
            self.session_input.text()
        )

        # Call the update_record function from the database
        update_record("Timetable", self.record_id, updated_data)

        QMessageBox.information(self, "Success", "Record updated successfully!")
        self.close()  # Close the update window

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Ensure QApplication is imported
    window = ViewTimetableWindow()
    window.show()
    sys.exit(app.exec_())

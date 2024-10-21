import sys
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, 
                             QLabel, QMessageBox, QApplication, 
                             QFormLayout, QLineEdit, QHeaderView)
from PyQt5.QtCore import pyqtSignal

def fetch_query_results(query):
    """Fetch results from the database based on the given query."""
    connection = sqlite3.connect('timetable.db')  # Update with your database file
    cursor = connection.cursor()
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    connection.close()
    return results

def delete_record(record_id, table_name):
    """Delete a record from the specified table."""
    connection = sqlite3.connect('timetable.db')  # Update with your database file
    cursor = connection.cursor()
    
    query = f"DELETE FROM {table_name} WHERE ID = ?"
    cursor.execute(query, (record_id,))
    
    connection.commit()
    connection.close()

class ViewTimetableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Timetable")
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout(self)
        self.showMaximized()

        # Create a label for debugging to confirm file connection
        self.debug_label = QLabel("Loading timetable data...", self)
        self.layout.addWidget(self.debug_label)

        # Create the table widget to display the timetable
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Load the timetable data from the database
        self.load_timetable_data()

    def load_timetable_data(self):
        """Load timetable data from the database and populate the table widget."""
        try:
            query = "SELECT * FROM Timetable"  # Updated to match the actual table name
            results = fetch_query_results(query)

            if results:
                self.debug_label.setText("Timetable data loaded successfully!")

                # Set up the table widget
                self.table_widget.setRowCount(len(results))
                self.table_widget.setColumnCount(len(results[0]) + 2)  # Adding space for buttons

                # Set table headers
                self.table_widget.setHorizontalHeaderLabels(['ID', 'Department', 'Semester', 'Teacher', 
                                                              'Course Title', 'Course Code', 'Classroom', 
                                                              'Start Time', 'End Time', 'Session', 'Update', 'Delete'])

                # Populate the table with data and buttons
                for row_index, row_data in enumerate(results):
                    for col_index, data in enumerate(row_data):
                        self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

                    # Create Update button
                    update_button = QPushButton("Update")
                    update_button.clicked.connect(lambda checked, id=row_data[0], data=row_data: self.open_update_window(id, data))
                    self.table_widget.setCellWidget(row_index, len(row_data), update_button)  # Last column for Update button

                    # Create Delete button
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda checked, id=row_data[0]: self.delete_record(id))
                    self.table_widget.setCellWidget(row_index, len(row_data) + 1, delete_button)  # Second last column for Delete button

            else:
                self.debug_label.setText("No timetable data available.")

        except Exception as e:
            self.debug_label.setText(f"Error loading timetable: {e}")

    def open_update_window(self, record_id, row_data):
        """Open the update window for the selected record."""
        self.update_window = UpdateTimetableWindow(record_id, row_data)  
        self.update_window.update_successful.connect(self.load_timetable_data)  # Connect signal to slot
        self.update_window.show()

    def delete_record(self, record_id):
        """Delete a record from the timetable."""
        reply = QMessageBox.question(self, 'Delete Confirmation', f"Are you sure you want to delete record ID {record_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_record(record_id, "Timetable")
            self.load_timetable_data()  # Reload the data to reflect changes

class UpdateTimetableWindow(QWidget):
    update_successful = pyqtSignal()

    def __init__(self, record_id, row_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Timetable Record")
        self.setGeometry(150, 150, 400, 300)

        self.record_id = record_id  
        self.row_data = row_data  
        self.parent = parent  

        self.layout = QFormLayout(self)

        # Create input fields for each column in the timetable
        self.department_input = QLineEdit(self)
        self.department_input.setText(row_data[1])  
        self.layout.addRow("Department:", self.department_input)

        self.semester_input = QLineEdit(self)
        self.semester_input.setText(row_data[2])  
        self.layout.addRow("Semester:", self.semester_input)

        self.teacher_input = QLineEdit(self)
        self.teacher_input.setText(row_data[3])  
        self.layout.addRow("Teacher:", self.teacher_input)

        self.course_title_input = QLineEdit(self)
        self.course_title_input.setText(row_data[4])  
        self.layout.addRow("Course Title:", self.course_title_input)

        self.course_code_input = QLineEdit(self)
        self.course_code_input.setText(row_data[5])  
        self.layout.addRow("Course Code:", self.course_code_input)

        self.classroom_input = QLineEdit(self)
        self.classroom_input.setText(row_data[6])  
        self.layout.addRow("Classroom:", self.classroom_input)

        self.start_time_input = QLineEdit(self)
        self.start_time_input.setText(row_data[7])  
        self.layout.addRow("Start Time:", self.start_time_input)

        self.end_time_input = QLineEdit(self)
        self.end_time_input.setText(row_data[8])  
        self.layout.addRow("End Time:", self.end_time_input)

        self.session_input = QLineEdit(self)
        self.session_input.setText(row_data[9])  
        self.layout.addRow("Session:", self.session_input)

        # Create Update button
        self.update_button = QPushButton("Update", self)
        self.update_button.clicked.connect(self.update_record)
        self.layout.addRow(self.update_button)

        self.setLayout(self.layout)

    def update_record(self):
        """Update the record in the database with the input values."""
        updated_data = (
            self.department_input.text(),
            self.semester_input.text(),
            self.teacher_input.text(),
            self.course_title_input.text(),
            self.course_code_input.text(),
            self.classroom_input.text(),
            self.start_time_input.text(),
            self.end_time_input.text(),
            self.session_input.text()
        )

        # Call the update_record function from the database
        update_record("Timetable", self.record_id, updated_data)
        self.update_successful.emit()
        QMessageBox.information(self, "Success", "Record updated successfully!")
        if self.parent:
            self.parent.load_timetable_data()
        self.close()

def update_record(table_name, record_id, updated_data):
    """Update a record in the specified table."""
    query = f"""UPDATE {table_name} 
                 SET department = ?,           
                     semester = ?, 
                     teacher = ?, 
                     course_title = ?,        
                     course_code = ?, 
                     classroom = ?, 
                     lecture_start_time = ?, 
                     lecture_end_time = ?, 
                     session = ? 
                 WHERE id = ?"""
    
    connection = sqlite3.connect('timetable.db')
    cursor = connection.cursor()

    try:
        cursor.execute(query, (*updated_data, record_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating record: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewTimetableWindow()
    window.show()
    sys.exit(app.exec_())

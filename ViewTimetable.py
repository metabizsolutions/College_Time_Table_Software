import sys
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel,
                             QMessageBox, QApplication, QFormLayout, 
                             QLineEdit, QHeaderView, QComboBox, QHBoxLayout, QFileDialog,QTimeEdit)
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QTime, QColor
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter, QFont,QPen
from datetime import datetime

def fetch_query_results(query, params=()):
    connection = sqlite3.connect('timetable.db')
    cursor = connection.cursor()
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    connection.close()
    return results

def delete_record(record_id, table_name):
    connection = sqlite3.connect('timetable.db')
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

        # Filters
        self.filter_layout = QHBoxLayout()
        self.department_filter = QComboBox(self)
        self.department_filter.addItem("All Departments")
        self.semester_filter = QComboBox(self)
        self.semester_filter.addItem("All Semesters")
        self.teacher_filter = QComboBox(self)
        self.teacher_filter.addItem("All Teachers")

        self.filter_layout.addWidget(QLabel("Department:", self))
        self.filter_layout.addWidget(self.department_filter)
        self.filter_layout.addWidget(QLabel("Semester:", self))
        self.filter_layout.addWidget(self.semester_filter)
        self.filter_layout.addWidget(QLabel("Teacher:", self))
        self.filter_layout.addWidget(self.teacher_filter)
        
        # Connect filter change to filtering function
        self.department_filter.currentIndexChanged.connect(self.apply_filters)
        self.semester_filter.currentIndexChanged.connect(self.apply_filters)
        self.teacher_filter.currentIndexChanged.connect(self.apply_filters)
        
        self.layout.addLayout(self.filter_layout)

        # Print Button
        self.print_button = QPushButton("Print to PDF", self)
        self.print_button.clicked.connect(self.print_to_pdf)
        self.layout.addWidget(self.print_button)

        # Debug label
        self.debug_label = QLabel("Loading timetable data...", self)
        self.layout.addWidget(self.debug_label)

        # Table widget
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Load data and filters
        self.load_filter_options()
        self.load_timetable_data()

    def load_filter_options(self):
        """Load unique filter options from the database into combo boxes."""
        try:
            # Populate Department filter
            departments = fetch_query_results("SELECT DISTINCT Department FROM Timetable")
            for department in departments:
                self.department_filter.addItem(department[0])

            # Populate Semester filter
            semesters = fetch_query_results("SELECT DISTINCT Semester FROM Timetable")
            for semester in semesters:
                self.semester_filter.addItem(semester[0])

            # Populate Teacher filter
            teachers = fetch_query_results("SELECT DISTINCT Teacher FROM Timetable")
            for teacher in teachers:
                self.teacher_filter.addItem(teacher[0])

        except Exception as e:
            self.debug_label.setText(f"Error loading filter options: {e}")

    def load_timetable_data(self):
        """Load timetable data from the database and populate the table widget."""
        try:
            query = "SELECT * FROM Timetable"
            results = fetch_query_results(query)

            if results:
                self.debug_label.setText("Timetable data loaded successfully!")
                self.populate_table(results)
            else:
                self.debug_label.setText("No timetable data available.")

        except Exception as e:
            self.debug_label.setText(f"Error loading timetable: {e}")

    def apply_filters(self):
        """Apply the selected filters and update the table display."""
        department = self.department_filter.currentText()
        semester = self.semester_filter.currentText()
        teacher = self.teacher_filter.currentText()

        # Build query with filters
        query = "SELECT * FROM Timetable WHERE 1=1"
        params = []

        if department != "All Departments":
            query += " AND Department = ?"
            params.append(department)
        
        if semester != "All Semesters":
            query += " AND Semester = ?"
            params.append(semester)
        
        if teacher != "All Teachers":
            query += " AND Teacher = ?"
            params.append(teacher)

        try:
            results = fetch_query_results(query, params)
            self.populate_table(results)

        except Exception as e:
            self.debug_label.setText(f"Error applying filters: {e}")

    def populate_table(self, results):
        """Populate the table widget with the provided results."""
        self.table_widget.setRowCount(len(results))
        self.table_widget.setColumnCount(len(results[0]) + 2)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Department', 'Semester', 'Teacher', 
                                                     'Course Title', 'Course Code', 'Classroom', 
                                                     'Start Time', 'End Time', 'Session', 'Update', 'Delete'])

        for row_index, row_data in enumerate(results):
            for col_index, data in enumerate(row_data):
                self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

            # Update button
            update_button = QPushButton("Update")
            update_button.clicked.connect(lambda checked, id=row_data[0], data=row_data: self.open_update_window(id, data))
            self.table_widget.setCellWidget(row_index, len(row_data), update_button)

            # Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, id=row_data[0]: self.delete_record(id))
            self.table_widget.setCellWidget(row_index, len(row_data) + 1, delete_button)











    def print_to_pdf(self):
        """Generate a PDF from the current table data."""
        # Open file dialog for the user to choose a save location
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        
        if not file_path:
            return  # User cancelled the save operation

        # Initialize printer
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPaperSize(QPrinter.A4)
        printer.setOutputFileName(file_path)

        # Set up QPainter to draw the table data
        painter = QPainter(printer)
        painter.begin(printer)

        # Define margins and available width
        margin_left = 50
        margin_top = 650
        margin_top = 300
        page_width = printer.pageRect().width() - 2 * margin_left
        page_height = printer.pageRect().height() - 2 * margin_top
        row_height = 600  # Set a fixed row height for all rows
        col_widths = [1200, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]  # Set column widths dynamically
        y_position = margin_top

        # Set title font
        painter.setFont(QFont("Arial", 14, QFont.Bold))

        # Calculate the width of the title text
        title_text = "Timetable"
        font_metrics = painter.fontMetrics()
        title_width = font_metrics.horizontalAdvance(title_text)

        # Calculate the x-position to center the text
        x_position = (page_width - title_width) / 2
        x_position = int(x_position)
        y_position = int(y_position)

        # Draw the title centered
        painter.drawText(x_position, y_position, title_text)

        # Adjust y-position after the title
        y_position += 350  # Space after the title

        # Set header font
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        x_position = margin_left
        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(1, self.table_widget.columnCount() - 2)]  # Exclude ID column
        for i, header in enumerate(headers):
            painter.drawText(x_position, y_position, header)
            x_position += col_widths[i]
        y_position += 450  # Space after headers

        # Set normal font for table rows
        painter.setFont(QFont("Arial", 9))

        for row in range(self.table_widget.rowCount()):
            x_position = margin_left

            for column in range(1, self.table_widget.columnCount() - 2):  # Exclude ID column
                item = self.table_widget.item(row, column)
                text = item.text() if item else ""

                # Format time columns in 12-hour format (if the column contains time data)
                if "time" in text.lower():  # Check if the text represents time
                    try:
                        # Parse the time in 24-hour format (assuming 'HH:MM' format)
                        time_obj = datetime.strptime(text, "%H:%M")  # 24-hour format
                        text = time_obj.strftime("%I:%M %p")  # Convert to 12-hour format (AM/PM)
                    except ValueError:
                        pass  # If it's not a valid time, leave it unchanged

                # Check if the column represents start time, end time, or starting time
                if "start_time" in self.table_widget.horizontalHeaderItem(column).text().lower():
                    # Format start time
                    try:
                        time_obj = datetime.strptime(text, "%H:%M")
                        text = time_obj.strftime("%I:%M %p")  # 12-hour format (AM/PM)
                    except ValueError:
                        pass
                elif "end_time" in self.table_widget.horizontalHeaderItem(column).text().lower():
                    # Format end time
                    try:
                        time_obj = datetime.strptime(text, "%H:%M")
                        text = time_obj.strftime("%I:%M %p")  # 12-hour format (AM/PM)
                    except ValueError:
                        pass
                elif "classroom" in self.table_widget.horizontalHeaderItem(column).text().lower():
                    # Leave the classroom text unchanged
                    pass
                elif "starting_time" in self.table_widget.horizontalHeaderItem(column).text().lower():
                    # Format the starting time if it's a time column
                    try:
                        time_obj = datetime.strptime(text, "%H:%M")
                        text = time_obj.strftime("%I:%M %p")  # 12-hour format (AM/PM)
                    except ValueError:
                        pass

                # Set the word wrap for text drawing and center the text in the cell
                text_options = Qt.TextWordWrap | Qt.AlignCenter  # Align text horizontally and vertically in the center

                # Define the rectangle for the cell with fixed row height
                cell_rect = QRect(x_position, y_position, col_widths[column - 1], row_height)

                # Draw the text inside the cell with word wrapping enabled
                painter.drawText(cell_rect, text_options, text)

                # Create a QPen with a thicker width for bold borders
                bold_pen = QPen(Qt.black)  # Use a black color for the borders; change if needed
                bold_pen.setWidth(3)  # Set the border width; adjust as desired for boldness

                # Set the pen on the painter
                painter.setPen(bold_pen)

                # Draw the cell borders with the bold pen
                painter.drawRect(cell_rect)

                # Increment x_position as before to move to the next cell
                x_position += col_widths[column - 1]


            # After processing all columns in the row, move the y-position down by the fixed row height
            y_position += row_height  # Move to the next row

            # Check if we need to fit the table in multiple pages
            if y_position > page_height - row_height:
                painter.end()
                printer.newPage()  # Start a new page
                painter.begin(printer)
                y_position = margin_top  # Reset the position for the new page

        painter.end()  # End the painting process

        # Display success message
        QMessageBox.information(self, "Success", f"PDF saved successfully at {file_path}")










    def open_update_window(self, record_id, row_data):
        self.update_window = UpdateTimetableWindow(record_id, row_data)  
        self.update_window.update_successful.connect(self.load_timetable_data)
        self.update_window.show()

    def delete_record(self, record_id):
        reply = QMessageBox.question(self, 'Delete Confirmation', f"Are you sure you want to delete record ID {record_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_record(record_id, "Timetable")
            self.load_timetable_data()

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

        # Department ComboBox populated from the database
        self.department_input = QComboBox(self)
        self.populate_combobox(self.department_input, "Department", row_data[1])
        self.layout.addRow("Department:", self.department_input)

        # Semester ComboBox populated from the database
        self.semester_input = QComboBox(self)
        self.populate_combobox(self.semester_input, "Semester", row_data[2])
        self.layout.addRow("Semester:", self.semester_input)

        # Teacher ComboBox populated from the database
        self.teacher_input = QComboBox(self)
        self.populate_combobox(self.teacher_input, "Teacher", row_data[3])
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

        # Use QTimeEdit for start time with 12-hour format
        self.start_time_input = QTimeEdit(self)
        self.start_time_input.setDisplayFormat("hh:mm AP")
        self.start_time_input.setTime(QTime.fromString(row_data[7], "hh:mm AP"))  # Set initial time
        self.layout.addRow("Start Time:", self.start_time_input)

        # Use QTimeEdit for end time with 12-hour format
        self.end_time_input = QTimeEdit(self)
        self.end_time_input.setDisplayFormat("hh:mm AP")
        self.end_time_input.setTime(QTime.fromString(row_data[8], "hh:mm AP"))  # Set initial time
        self.layout.addRow("End Time:", self.end_time_input)

        self.session_input = QLineEdit(self)
        self.session_input.setText(row_data[9])  
        self.layout.addRow("Session:", self.session_input)

        self.update_button = QPushButton("Update", self)
        self.update_button.clicked.connect(self.update_record)
        self.layout.addRow(self.update_button)

        self.setLayout(self.layout)

    def populate_combobox(self, combo_box, column_name, current_value):
        """Populate the combo box with data from the database."""
        query = f"SELECT DISTINCT {column_name} FROM Timetable"
        values = fetch_query_results(query)

        # Add 'All' option for non-specific filtering
        combo_box.addItem(f"All {column_name}s")
        
        for value in values:
            combo_box.addItem(value[0])
        
        # Set the current value from the record if available
        if current_value:
            index = combo_box.findText(current_value)
            if index != -1:
                combo_box.setCurrentIndex(index)

    def update_record(self):
        updated_data = (
            self.department_input.currentText(),
            self.semester_input.currentText(),
            self.teacher_input.currentText(),
            self.course_title_input.text(),
            self.course_code_input.text(),
            self.classroom_input.text(),
            self.start_time_input.time().toString("hh:mm AP"),  # Get selected start time
            self.end_time_input.time().toString("hh:mm AP"),    # Get selected end time
            self.session_input.text()
        )

        update_record("Timetable", self.record_id, updated_data)
        self.update_successful.emit()
        QMessageBox.information(self, "Success", "Record updated successfully!")
        if self.parent:
            self.parent.load_timetable_data()
        self.close()


def update_record(table_name, record_id, updated_data):
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

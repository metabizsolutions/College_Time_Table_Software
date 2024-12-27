import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WorkloadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workload Management")
        self.setGeometry(100, 100, 1200, 800)  # Fullscreen
        self.showMaximized()

        # Connect to the database
        self.conn = sqlite3.connect('timetable.db')
        self.cursor = self.conn.cursor()

        # Set up layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add title label
        self.title_label = QLabel("Teacher Workload")
        self.title_label.setFont(QFont("Georgia", 24))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Add search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a teacher...")
        self.search_bar.setFont(QFont("Georgia", 14))
        self.search_bar.textChanged.connect(self.filter_table)  # Connect search input to filter function
        self.layout.addWidget(self.search_bar)

        # Add table widget
        self.workload_table = QTableWidget()
        self.layout.addWidget(self.workload_table)

        # Populate the table with data
        self.populate_workload_table()

    def populate_workload_table(self):
        # Query to calculate workload and group by teacher, department, and semester
        query = """
        SELECT 
            teacher, 
            GROUP_CONCAT(DISTINCT department || ' (' || semester || ')') AS department_semester,
            COUNT(*) AS total_lectures,
            COUNT(*) * 1.5 AS workload
        FROM Timetable
        GROUP BY teacher
        """

        self.cursor.execute(query)
        self.results = self.cursor.fetchall()  # Store results for filtering

        # Set up the table structure
        self.workload_table.setRowCount(len(self.results))
        self.workload_table.setColumnCount(4)
        self.workload_table.setHorizontalHeaderLabels(["Teacher", "Department & Semesters", "Total Lectures", "Workload (Hours)"])
        self.workload_table.setFont(QFont("Georgia", 12))

        # Fill the table with data
        for row_index, row_data in enumerate(self.results):
            teacher, department_semesters, total_lectures, workload = row_data

            teacher_item = QTableWidgetItem(teacher)
            department_item = QTableWidgetItem(department_semesters)
            total_lectures_item = QTableWidgetItem(str(total_lectures))
            workload_item = QTableWidgetItem(f"{workload:.2f}")

            # Enable text wrapping and adjust row height
            teacher_item.setTextAlignment(Qt.AlignTop)
            department_item.setTextAlignment(Qt.AlignTop)
            total_lectures_item.setTextAlignment(Qt.AlignTop)
            workload_item.setTextAlignment(Qt.AlignTop)

            teacher_item.setFlags(teacher_item.flags() ^ Qt.ItemIsEditable)
            department_item.setFlags(department_item.flags() ^ Qt.ItemIsEditable)
            total_lectures_item.setFlags(total_lectures_item.flags() ^ Qt.ItemIsEditable)
            workload_item.setFlags(workload_item.flags() ^ Qt.ItemIsEditable)

            # Enable word wrap
            teacher_item.setFont(QFont("Georgia", 12))
            department_item.setFont(QFont("Georgia", 12))
            total_lectures_item.setFont(QFont("Georgia", 12))
            workload_item.setFont(QFont("Georgia", 12))

            # Add items to the table
            self.workload_table.setItem(row_index, 0, teacher_item)
            self.workload_table.setItem(row_index, 1, department_item)
            self.workload_table.setItem(row_index, 2, total_lectures_item)
            self.workload_table.setItem(row_index, 3, workload_item)

            # Resize columns and rows based on content
            self.workload_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.workload_table.resizeRowsToContents()


    def filter_table(self):
        search_text = self.search_bar.text().lower()

        # Filter results based on search text
        filtered_results = [
            row for row in self.results if search_text in row[0].lower()
        ]

        # Update table rows based on filtered results
        self.workload_table.setRowCount(len(filtered_results))
        for row_index, row_data in enumerate(filtered_results):
            teacher, department_semesters, total_lectures, workload = row_data

            teacher_item = QTableWidgetItem(teacher)
            department_item = QTableWidgetItem(department_semesters)
            total_lectures_item = QTableWidgetItem(str(total_lectures))
            workload_item = QTableWidgetItem(f"{workload:.2f}")

            # Enable text wrapping for all items
            teacher_item.setTextAlignment(Qt.AlignTop)
            department_item.setTextAlignment(Qt.AlignTop)
            total_lectures_item.setTextAlignment(Qt.AlignTop)
            workload_item.setTextAlignment(Qt.AlignTop)

            teacher_item.setFlags(teacher_item.flags() ^ Qt.ItemIsEditable)
            department_item.setFlags(department_item.flags() ^ Qt.ItemIsEditable)
            total_lectures_item.setFlags(total_lectures_item.flags() ^ Qt.ItemIsEditable)
            workload_item.setFlags(workload_item.flags() ^ Qt.ItemIsEditable)

            # Add items to the table
            self.workload_table.setItem(row_index, 0, teacher_item)
            self.workload_table.setItem(row_index, 1, department_item)
            self.workload_table.setItem(row_index, 2, total_lectures_item)
            self.workload_table.setItem(row_index, 3, workload_item)

        # Reset column width proportions after updating rows
        self.workload_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.workload_table.resizeRowsToContents()


def main():
    app = QApplication(sys.argv)
    window = WorkloadWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

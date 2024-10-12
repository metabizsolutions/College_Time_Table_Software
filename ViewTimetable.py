from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from database import fetch_query_results  # Assuming this function fetches data from your database

class ViewTimetableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Timetable")
        self.setGeometry(100, 100, 600, 400)
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
                self.table_widget.setColumnCount(len(results[0]))  # Assuming all rows have the same columns

                # Set table headers (adjust according to your table's columns)
                self.table_widget.setHorizontalHeaderLabels(['Class', 'Course', 'Teacher', 'Day', 'Time'])

                # Populate the table with data
                for row_index, row_data in enumerate(results):
                    for col_index, data in enumerate(row_data):
                        self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(data)))
            else:
                self.debug_label.setText("No timetable data available.")
                print("No data found in the timetable.")

        except Exception as e:
            self.debug_label.setText(f"Error loading timetable: {e}")
            print(f"Error loading timetable: {e}")

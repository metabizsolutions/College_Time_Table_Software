import sqlite3
import sys
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QComboBox, QLabel,
    QPushButton, QMessageBox, QDesktopWidget
)
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta

# Simulated database query function
def fetch_query_results(query, params=()):
    """Fetch results from the SQLite database."""
    connection = sqlite3.connect("timetable.db")  # Connect to the database
    cursor = connection.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    connection.close()
    return results

class GenerateReportWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Timetable Generator")
        self.setGeometry(100, 100, 1200, 700)
        self.center_window()

        # Set up the layout
        self.main_layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("College Timetable Generator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(title_label)

        # Create a form layout for department selection
        self.form_layout = QFormLayout()
        self.department_label = QLabel("Select Department:")
        self.department_combo = QComboBox()
        self.department_combo.addItems(["All Departments"] + self.get_departments())  # Add "All Departments"
        self.form_layout.addRow(self.department_label, self.department_combo)

        # Add form layout to the main layout
        self.main_layout.addLayout(self.form_layout)

        # Button to generate timetable
        self.generate_button = QPushButton("Generate Timetable")
        self.generate_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.generate_button.clicked.connect(self.generate_html_timetable)
        self.main_layout.addWidget(self.generate_button)

        # Set the main layout
        self.setLayout(self.main_layout)

    def center_window(self):
        """Center the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_departments(self):
        """Fetch distinct departments from the Programs table."""
        query = "SELECT DISTINCT program_name FROM Programs"
        departments = fetch_query_results(query)
        return [department[0] for department in departments]

    def generate_html_timetable(self):
        """Generate and open the timetable as an HTML file."""
        department = self.department_combo.currentText()

        if department == "All Departments":
            # Fetch timetable data for all departments
            timetable_data = self.get_all_timetable_data()
        else:
            if not department:
                QMessageBox.warning(self, "Input Error", "Please select a department.")
                return

            # Fetch timetable data for the selected department
            timetable_data = self.get_timetable_data_for_department(department)

        if not timetable_data:
            QMessageBox.warning(self, "No Data", "No data found for the selected department.")
            return

        # Generate the HTML content for the selected department
        html_content = self.create_html_table(timetable_data, department)

        # Save the HTML file
        file_name = "timetable.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Open the HTML file in the default web browser
        webbrowser.open(file_name)
        QMessageBox.information(self, "Success", "Timetable generated and opened in your browser.")

    def create_html_table(self, data, department):
        """Generate the HTML table structure with pagination (5 departments per page) and session-wise grouping."""
        # Extract unique time slots and sort by time
        time_slots = self.generate_time_slots(data)  # Generate 8 time slots dynamically

        # Get the current date in the desired format
        current_date = datetime.now().strftime("%d-%m-%Y")

        # Group data by session (morning first, then evening)
        sessions = set(row[8] for row in data)  # Get unique sessions
        sessions = sorted(sessions, key=lambda x: 0 if x == "Morning" else 1)  # Morning first

        # Start HTML structure
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Timetable for {department}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid black; padding: 10px; text-align: center; }}
                th {{ background-color: #f8f8f8; font-weight: bold; }}
                h2, h4 {{ text-align: center; margin-bottom: 20px; }}
                .footer-text {{ text-align: center; margin-top: 30px; font-size: 14px; }}
                .footer-text p {{ margin: 5px; }}
                .page-break {{ page-break-after: always; }} /* Add page break after each table */
            </style>
        </head>
        <body>
        """

        # Generate tables for each session (morning first, then evening)
        for session in sessions:
            # Filter data for the current session
            session_data = [row for row in data if row[8] == session]

            # Group data by semester within the session
            semesters = set(row[7] for row in session_data)  # Get unique semesters
            semesters = sorted(semesters)  # Sort semesters in ascending order

            # Generate tables for each semester in the current session
            for sem in semesters:
                # Filter data for the current semester and session
                semester_data = [row for row in session_data if row[7] == sem]

                # Group data by department and classroom
                departments = set((row[0], row[1]) for row in semester_data)
                departments = sorted(departments, key=lambda x: x[0])  # Sort by department name

                # Split departments into chunks of 5 per page
                chunk_size = 5
                department_chunks = [departments[i:i + chunk_size] for i in range(0, len(departments), chunk_size)]

                # Add header for the semester and session
                html += f"""
                <h2>Timetable for {department} - Semester {sem} ({session})</h2>
                <h4>Government Graduate College Muzaffargarh</h4>
                """

                # Generate a table for each chunk of departments
                for chunk_index, chunk in enumerate(department_chunks):
                    # Start table
                    html += "<table>"
                    html += "<thead><tr><th>Department</th><th>Classroom</th>"
                    # Add time slots as headers
                    for start, end in time_slots:
                        html += f"<th>{start} - {end}</th>"
                    html += "</tr></thead><tbody>"

                    # Populate rows for each department and classroom in the chunk
                    for department_name, classroom in chunk:
                        html += f"<tr><td>{department_name}</td><td>{classroom}</td>"

                        # Add lecture details for each time slot
                        for start, end in time_slots:
                            # Find all lectures for this department, classroom, and time slot
                            lectures = [
                                row for row in semester_data
                                if row[0] == department_name and row[1] == classroom and row[5] == start and row[6] == end
                            ]
                            if lectures:
                                # Combine all lectures into a single cell
                                lecture_details = "<br>".join(
                                    f"{lecture[2]} ({lecture[3]}) - {lecture[4]}"
                                    for lecture in lectures
                                )
                                html += f"<td>{lecture_details}</td>"
                            else:
                                # If no lecture, leave the cell empty
                                html += "<td></td>"
                        html += "</tr>"

                    html += "</tbody></table>"

                    # Add footer for each page
                    html += f"""
                    <div class="footer-text">
                        <p>Generated on ({current_date})</p>
                        <p>Prof. Muhammad Adnan Saeed - Incharge College Timetable</p>
                        <p>Prof. Dr. Rahmat Ullah - Principal</p>
                    </div>
                    """

                    # Add a page break after each table (except the last one for the semester)
                    if chunk_index < len(department_chunks) - 1:
                        html += '<div class="page-break"></div>'

                # Add a page break after each semester (except the last one in the session)
                if sem != semesters[-1]:
                    html += '<div class="page-break"></div>'

            # Add a page break after each session (except the last one)
            if session != sessions[-1]:
                html += '<div class="page-break"></div>'

        # Close HTML structure
        html += """
        </body>
        </html>
        """
        return html

    def generate_time_slots(self, data):
        """Generate 8 time slots based on the starting time and lecture duration."""
        # Fetch the starting time and lecture duration from the first record
        if not data:
            return []

        start_time_str = data[0][5]  # Fetch starting time from the first record
        lecture_duration = data[0][9]  # Fetch lecture duration from the first record

        # Handle cases where lecture_duration is None
        if lecture_duration is None:
            lecture_duration = 50  # Default duration in minutes (you can change this as needed)

        # Convert start time to a datetime object
        try:
            start_time = datetime.strptime(start_time_str, "%I:%M %p")
        except ValueError:
            # Handle invalid time format
            start_time = datetime.strptime("08:00 AM", "%I:%M %p")  # Default start time

        # Generate 8 time slots
        time_slots = []
        for i in range(8):
            end_time = start_time + timedelta(minutes=lecture_duration)
            time_slots.append((
                start_time.strftime("%I:%M %p"),  # Format as 12-hour time with AM/PM
                end_time.strftime("%I:%M %p")
            ))
            start_time = end_time  # Move to the next slot

        return time_slots

    def get_timetable_data_for_department(self, department):
        """Fetch all timetable data for the selected department."""
        query = """
            SELECT department, classroom, course_title, course_code, teacher, 
                   lecture_start_time, lecture_end_time, semester, session, lecture_duration
            FROM Timetable 
            WHERE department = ?
            ORDER BY session, classroom, lecture_start_time
        """
        return fetch_query_results(query, (department,))

    def get_all_timetable_data(self):
        """Fetch all timetable data for all departments."""
        query = """
            SELECT department, classroom, course_title, course_code, teacher, 
                   lecture_start_time, lecture_end_time, semester, session, lecture_duration
            FROM Timetable 
            ORDER BY 
                session ASC,                 -- Morning first (assumes 'Morning' < 'Evening')
                department ASC,              -- Sort by department
                classroom ASC,               -- Sort by classroom
                lecture_start_time ASC       -- Sort by lecture start time
        """
        return fetch_query_results(query)

def main():
    app = QApplication(sys.argv)
    window = GenerateReportWindow()
    window.showMaximized()  # Open the window in full-screen mode
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
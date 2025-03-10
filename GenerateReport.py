import sqlite3
import sys
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QComboBox, QLabel,
    QPushButton, QMessageBox, QDesktopWidget
)
from PyQt5.QtCore import Qt
from datetime import datetime

# Simulated database query function
def fetch_query_results(query, params=()):
    """Simulates fetching results from a database."""
    connection = sqlite3.connect("timetable.db")  # Replace with your database file
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

        # Create a form layout for semester selection
        self.form_layout = QFormLayout()
        self.semester_label = QLabel("Select Semester:")
        self.semester_combo = QComboBox()
        self.semester_combo.addItems(["All Semesters"] + self.get_semesters())  # Add "All Semesters"
        self.form_layout.addRow(self.semester_label, self.semester_combo)

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

    def get_semesters(self):
        """Fetch distinct semesters from the Timetable table."""
        query = "SELECT DISTINCT semester FROM Timetable"
        semesters = fetch_query_results(query)
        return [semester[0] for semester in semesters]

    def generate_html_timetable(self):
        """Generate and open the timetable as an HTML file."""
        semester = self.semester_combo.currentText()

        if semester == "All Semesters":
            # Fetch timetable data for all semesters
            timetable_data = self.get_all_timetable_data()

            if not timetable_data:
                QMessageBox.warning(self, "No Data", "No data found for any semester.")
                return

            # Generate the HTML content for all semesters
            html_content = self.create_html_table(timetable_data, semester="All Semesters")
        else:
            if not semester:
                QMessageBox.warning(self, "Input Error", "Please select a semester.")
                return

            # Fetch timetable data for the selected semester
            timetable_data = self.get_departments_classrooms_and_courses_for_semester(semester)

            if not timetable_data:
                QMessageBox.warning(self, "No Data", "No data found for the selected semester.")
                return

            # Generate the HTML content for the selected semester
            html_content = self.create_html_table(timetable_data, semester)

        # Save the HTML file
        file_name = "timetable.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Open the HTML file in the default web browser
        webbrowser.open(file_name)
        QMessageBox.information(self, "Success", "Timetable generated and opened in your browser.")

    def create_html_table(self, data, semester):
        """Generate the HTML table structure with pagination (5 departments per page) and session-wise grouping."""
        # Extract unique time slots and sort by time
        time_slots = sorted(set((start, end) for _, _, _, _, _, start, end, _, _ in data), 
                        key=lambda x: datetime.strptime(x[0], "%I:%M %p"))

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
            <title>Timetable for {semester}</title>
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
            semesters = sorted(semesters)  # Sort semesters

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
                <h2>Timetable for {sem} ({session})</h2>
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
                    for department, classroom in chunk:
                        html += f"<tr><td>{department}</td><td>{classroom}</td>"

                        # Add lecture details for each time slot
                        for start, end in time_slots:
                            # Find all lectures for this department, classroom, and time slot
                            lectures = [
                                row for row in semester_data
                                if row[0] == department and row[1] == classroom and row[5] == start and row[6] == end
                            ]
                            if lectures:
                                # Combine all lectures into a single cell
                                lecture_details = "<br>".join(
                                    f"{lecture[2]} ({lecture[3]}) - {lecture[4]}"
                                    for lecture in lectures
                                )
                                html += f"<td>{lecture_details}</td>"
                            else:
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

    def get_departments_classrooms_and_courses_for_semester(self, semester):
        """Fetch all timetable data for the selected semester."""
        query = """
            SELECT department, classroom, course_title, course_code, teacher, 
                   lecture_start_time, lecture_end_time, semester, session
            FROM Timetable 
            WHERE semester = ?
            ORDER BY department, classroom, lecture_start_time
        """
        return fetch_query_results(query, (semester,))

    def get_all_timetable_data(self):
        """Fetch all timetable data for all semesters."""
        query = """
            SELECT department, classroom, course_title, course_code, teacher, 
                   lecture_start_time, lecture_end_time, semester, session
            FROM Timetable 
            ORDER BY 
                session ASC,                 -- Morning first (assumes 'Morning' < 'Evening')
                semester ASC,                -- Sort by semester
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
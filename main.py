import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import database  # Make sure this imports your database functions correctly

class TimetableCreationWindow(QWidget):
    def __init__(self, db_name, timetable_type):
        super().__init__()
        self.setWindowTitle(f"Create {timetable_type} Timetable")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("background-color: #49bcfc;")  # Background color

        layout = QVBoxLayout(self)

        # Add logo in the center
        self.add_logo(layout)

        # Header label
        label = QLabel(f"Create {timetable_type} Timetable")
        label.setFont(QFont("Arial", 28, QFont.Bold))  # Increased font size
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        # Add form fields
        self.add_form_fields(layout)

        # Generate Timetable button
        generate_btn = QPushButton("Generate Timetable")
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #181818;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 18px;  # Button text size
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        generate_btn.setFont(QFont("Georgia", 18, QFont.Bold))  # Button font size
        generate_btn.setFixedSize(300, 60)

        layout.addWidget(generate_btn, alignment=Qt.AlignCenter)  # Align the button using the layout

        # Add new action buttons below "Generate Timetable"
        self.add_action_buttons(layout)

        self.setLayout(layout)

    def add_logo(self, layout):
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")  # Adjust path to your logo
        logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

    def add_form_fields(self, layout):
        form_layout = QVBoxLayout()

        # Create horizontal layouts for each row of input fields
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        # Fetch data from the database
        classrooms = self.fetch_data_from_database("SELECT classroom_name FROM Classrooms")
        teachers = self.fetch_data_from_database("SELECT teacher_name FROM Teachers")
        courses = self.fetch_data_from_database("SELECT course_name, course_code FROM Courses")
        programs = self.fetch_data_from_database("SELECT program_name, semester FROM Programs")

        # Create and populate the dropdowns for the first row
        self.classroom_combobox = self.create_combobox("Select Classroom", [classroom[0] for classroom in classrooms], hbox1)
        self.teacher_combobox = self.create_combobox("Select Teacher", [teacher[0] for teacher in teachers], hbox1)
        self.course_combobox = self.create_combobox("Select Course Title", [course[0] for course in courses], hbox1)

        # Create and populate the dropdowns for the second row
        self.code_combobox = self.create_combobox("Select Code", [course[1] for course in courses], hbox2)
        self.program_combobox = self.create_combobox("Select Program", [program[0] for program in programs], hbox2)
        self.semester_combobox = self.create_combobox("Select Semester", [program[1] for program in programs], hbox2)

        # Add both horizontal layouts to the form layout
        form_layout.addLayout(hbox1)
        form_layout.addLayout(hbox2)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)
        layout.setAlignment(form_layout, Qt.AlignCenter)  # Set alignment separately

    def create_combobox(self, label_text, items, layout):
        label = QLabel(label_text)
        label.setStyleSheet("color: white;")
        label.setFont(QFont("Arial", 16))  # Set font size for labels

        combobox = QComboBox()
        combobox.addItems(items)
        combobox.setFixedSize(250, 40)  # Set a standard size for the combo boxes
        layout.addWidget(label)
        layout.addWidget(combobox)

        return combobox

    def fetch_data_from_database(self, query):
        return database.fetch_data(query)  # Make sure this function exists in database.py

    def add_action_buttons(self, layout):
        button_layout = QVBoxLayout()

        # Create the buttons with the same style and size as "Generate Timetable"
        overall_btn = QPushButton("Print Overall Timetable")
        dept_btn = QPushButton("Print Dept Timetable")
        overload_btn = QPushButton("Print Work Overload")

        # Apply the same style and size as the "Generate Timetable" button
        for btn in [overall_btn, dept_btn, overload_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #181818;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            btn.setFont(QFont("Georgia", 18, QFont.Bold))
            btn.setFixedSize(300, 60)

        # Add buttons to the layout
        button_layout.addWidget(overall_btn, alignment=Qt.AlignCenter)
        button_layout.addWidget(dept_btn, alignment=Qt.AlignCenter)
        button_layout.addWidget(overload_btn, alignment=Qt.AlignCenter)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Connect the buttons to their respective functions (placeholders for now)
        overall_btn.clicked.connect(self.print_overall_timetable)
        dept_btn.clicked.connect(self.print_dept_timetable)
        overload_btn.clicked.connect(self.print_work_overload)

    def print_overall_timetable(self):
        # Placeholder function for printing overall timetable
        print("Printing overall timetable")

    def print_dept_timetable(self):
        # Placeholder function for printing dept timetable
        print("Printing department timetable")

    def print_work_overload(self):
        # Placeholder function for printing work overload
        print("Printing work overload")


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Timetable Management System")
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #49bcfc;")

        self.add_logo()
        self.init_ui()

    def add_logo(self):
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")  # Load logo image
        logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label, alignment=Qt.AlignCenter)

    def init_ui(self):
        label = QLabel("Create Timetable")
        label.setFont(QFont("Georgia", 28, QFont.Bold))  # Increased font size for main title
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        morning_btn = QPushButton("Morning Classes")
        evening_btn = QPushButton("Evening Classes")

        button_style = """
            QPushButton {
                background-color: #181818;
                color: white;
                border-radius: 10px;
                padding: 10px; 
                font-size: 18px;  # Button text size
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
        morning_btn.setStyleSheet(button_style)
        evening_btn.setStyleSheet(button_style)

        button_font = QFont("Georgia", 18, QFont.Bold)  # Increased button font size
        morning_btn.setFont(button_font)
        evening_btn.setFont(button_font)

        morning_btn.setFixedSize(300, 60)
        evening_btn.setFixedSize(300, 60)

        self.layout.setSpacing(3)

        self.layout.addWidget(morning_btn, alignment=Qt.AlignCenter)
        self.layout.addWidget(evening_btn, alignment=Qt.AlignCenter)

        morning_btn.clicked.connect(lambda: self.create_timetable("Morning"))
        evening_btn.clicked.connect(lambda: self.create_timetable("Evening"))

        label = QLabel("Developed by: MetaBiz Solution")
        label.setFont(QFont("Georgia", 14))  # Set font size for the developer label
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

    def create_timetable(self, timetable_type):
        db_name = "timetable.db"
        self.check_and_open_timetable(db_name, timetable_type)

    def check_and_open_timetable(self, db_name, timetable_type):
        if not os.path.exists(db_name):
            self.show_error_message("Database not found", "The required database was not found.")
        else:
            self.timetable_window = TimetableCreationWindow(db_name, timetable_type)
            self.timetable_window.show()

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())

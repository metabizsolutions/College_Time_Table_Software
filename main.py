import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from AddData import AddDataWindow
from ViewTimetable import ViewTimetableWindow
from UpdateData import UpdateDataWindow
from UpdateData import MainWindow
from CreateTimetable import CreateTimetableWindow
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QComboBox, QMessageBox, QFormLayout, QScrollArea
import sqlite3
class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("College Timetable Management System")
        self.setGeometry(200, 200, 800, 600)
        self.showMaximized() 
        

        # Set sky blue background
        self.setStyleSheet("background-color: skyblue;")

        # Create a vertical layout to center the content
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)  # Align the layout to the center

        # Add a logo at the top of the window
        self.add_logo()

        # Add buttons
        self.add_buttons()

        # Add footer
        self.add_footer()

        self.show()

    def add_logo(self):
        # Add a label for the logo and center it
        self.logo_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("logo.png")  # Assuming you have a logo.png file
        self.logo_label.setPixmap(pixmap.scaled(400, 200, QtCore.Qt.KeepAspectRatio))  # Enlarged logo
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)  # Align the logo in the center
        self.layout.addWidget(self.logo_label)

    def add_buttons(self):
        # Create a widget to hold buttons and center them
        self.button_widget = QtWidgets.QWidget(self)
        self.button_layout = QtWidgets.QVBoxLayout(self.button_widget)
        self.button_layout.setAlignment(QtCore.Qt.AlignCenter)  # Center buttons vertically
        self.button_widget.setLayout(self.button_layout)

        # Button style with increased width
        button_style = """
            QPushButton {
                background-color: #181818;
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                width: 300px;  /* Set standard width */
            }
            QPushButton:hover {
                background-color: #0056b3;
                border: 2px solid #ffffff;
            }
        """

        # Create buttons with styles
        self.view_timetable_button = QtWidgets.QPushButton("View Timetable")
        self.view_timetable_button.setStyleSheet(button_style)
        self.view_timetable_button.clicked.connect(self.open_view_timetable_window)
        self.button_layout.addWidget(self.view_timetable_button)

        self.add_data_button = QtWidgets.QPushButton("Add New Data")
        self.add_data_button.setStyleSheet(button_style)
        self.add_data_button.clicked.connect(self.open_add_data_window)
        self.button_layout.addWidget(self.add_data_button)

        self.update_data_button = QtWidgets.QPushButton("Update Data")
        self.update_data_button.setStyleSheet(button_style)
        self.update_data_button.clicked.connect(self.open_update_data_window)
        self.button_layout.addWidget(self.update_data_button)

        self.create_timetable_button = QtWidgets.QPushButton("Create Timetable")
        self.create_timetable_button.setStyleSheet(button_style)
        self.create_timetable_button.clicked.connect(self.open_create_timetable_window)
        self.button_layout.addWidget(self.create_timetable_button)




        # Add the button widget to the main layout
        self.layout.addWidget(self.button_widget)

    def add_footer(self):
        footer_label = QtWidgets.QLabel("Developed by MetaBiz Solutions", self)
        footer_label.setAlignment(QtCore.Qt.AlignCenter)
        footer_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black; padding: 10px;")
        self.layout.addWidget(footer_label)

    def open_add_data_window(self):
        # Create a new window
        self.add_data_window = QMainWindow()
        self.add_data_window.setWindowTitle("Add Data - Modern Interface")

        # Maximize the window
        self.add_data_window.showMaximized()

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a container widget to hold the form layout
        container_widget = QWidget()

        # Create a form layout
        layout = QFormLayout(container_widget)

        # Set modern styles for fonts and buttons
        label_font = QFont("Tahoma", 14, QFont.Bold)

        # Style for input fields
        textbox_style = """
        QLineEdit {
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
            margin-bottom: 20px;
        }
        """

        # Style for buttons
        button_style = """
        QPushButton {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        """

        # Add Classroom Section

        #Add Classroom label
        self.label_classroom = QLabel("CLASSROOM")
        self.label_classroom.setFont(label_font)
        layout.addRow(self.label_classroom)
        self.textbox_classroom = QLineEdit()
        self.textbox_classroom.setStyleSheet(textbox_style)
        self.textbox_classroom.setPlaceholderText("Add Classroom")
        self.textbox_classroom.setFixedWidth(300)  # Set fixed width for the textbox
        self.btn_add_classroom = QPushButton("Add Classroom")
        self.btn_add_classroom.setStyleSheet(button_style)
        self.btn_add_classroom.setFixedWidth(300)  # Set fixed width for the button
        self.btn_add_classroom.clicked.connect(self.add_classroom)
        layout.addRow(self.textbox_classroom)
        layout.addRow("", self.btn_add_classroom)
        # Center align specific rows
        layout.setAlignment(self.label_classroom, Qt.AlignCenter)
        layout.setAlignment(self.textbox_classroom, Qt.AlignCenter)
        layout.setAlignment(self.btn_add_classroom, Qt.AlignCenter)




        # Add Course Section

        self.label_course = QLabel("COURSE")
        self.label_course.setFont(label_font)
        self.textbox_course_name = QLineEdit()
        self.textbox_course_code = QLineEdit()
        self.textbox_course_credits = QLineEdit()
        self.textbox_course_name.setPlaceholderText("Course Name")
        self.textbox_course_code.setPlaceholderText("Course Code")
        self.textbox_course_credits.setPlaceholderText("Credits")
        self.textbox_course_name.setStyleSheet(textbox_style)
        self.textbox_course_code.setStyleSheet(textbox_style)
        self.textbox_course_credits.setStyleSheet(textbox_style)
        self.textbox_course_name.setFixedWidth(300)
        self.textbox_course_code.setFixedWidth(300)
        self.textbox_course_credits.setFixedWidth(300)
        self.btn_add_course = QPushButton("Add Course")
        self.btn_add_course.setStyleSheet(button_style)
        self.btn_add_course.setFixedWidth(300)
        self.btn_add_course.clicked.connect(self.add_course)

        layout.addRow(self.label_course)
        layout.addRow(self.textbox_course_name)
        layout.addRow(self.textbox_course_code)
        layout.addRow(self.textbox_course_credits)
        layout.addRow("", self.btn_add_course)

        layout.setAlignment(self.label_course, Qt.AlignCenter)
        layout.setAlignment(self.textbox_course_name, Qt.AlignCenter)
        layout.setAlignment(self.textbox_course_code, Qt.AlignCenter)
        layout.setAlignment(self.textbox_course_credits, Qt.AlignCenter)
        layout.setAlignment(self.btn_add_course, Qt.AlignCenter)




        # Add Day Section

        self.label_day = QLabel("DAY")
        self.label_day.setFont(label_font)
        self.combobox_day = QComboBox()
        self.combobox_day.setStyleSheet(textbox_style)
        self.combobox_day.addItems(["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"])
        self.combobox_day.setFixedWidth(300)
        self.btn_add_day = QPushButton("Add Day")
        self.btn_add_day.setStyleSheet(button_style)
        self.btn_add_day.setFixedWidth(300)
        self.btn_add_day.clicked.connect(self.add_day)

        layout.addRow(self.label_day)
        layout.addRow( self.combobox_day)
        layout.addRow("", self.btn_add_day)

        layout.setAlignment(self.label_day, Qt.AlignCenter)
        layout.setAlignment(Qt.AlignCenter)
        layout.setAlignment(self.combobox_day, Qt.AlignCenter)
        layout.setAlignment(self.btn_add_day, Qt.AlignCenter)





        # Add Program Section

        self.label_classroom_program = QLabel("PROGRAM")
        self.label_classroom_program.setFont(label_font)
        self.textbox_program_name = QLineEdit()
        self.textbox_program_semester = QLineEdit()
        self.textbox_program_name.setPlaceholderText("Program Name")
        self.textbox_program_semester.setPlaceholderText("Semester")
        self.textbox_program_name.setStyleSheet(textbox_style)
        self.textbox_program_semester.setStyleSheet(textbox_style)
        self.textbox_program_name.setFixedWidth(300)
        self.textbox_program_semester.setFixedWidth(300)
        self.btn_add_program = QPushButton("Add Program")
        self.btn_add_program.setStyleSheet(button_style)
        self.btn_add_program.setFixedWidth(300)
        self.btn_add_program.clicked.connect(self.add_program)


        layout.addRow(self.label_classroom_program)
        layout.addRow(self.textbox_program_name)
        layout.addRow(self.textbox_program_semester)
        layout.addRow("", self.btn_add_program)

        layout.setAlignment(self.label_classroom_program, Qt.AlignCenter)
        layout.setAlignment(self.textbox_program_name, Qt.AlignCenter)
        layout.setAlignment(self.textbox_program_semester, Qt.AlignCenter)
        layout.setAlignment(self.btn_add_program, Qt.AlignCenter)





        # Add Teacher Section

        self.label_teacher = QLabel("TEACHER")
        self.label_teacher.setFont(label_font)
        self.textbox_teacher_name = QLineEdit()
        self.textbox_teacher_bps = QLineEdit()
        self.textbox_teacher_specialization = QLineEdit()
        self.textbox_teacher_name.setPlaceholderText("Teacher Name")
        self.textbox_teacher_bps.setPlaceholderText("BPS Grade")
        self.textbox_teacher_specialization.setPlaceholderText("Specialization")
        self.textbox_teacher_name.setStyleSheet(textbox_style)
        self.textbox_teacher_bps.setStyleSheet(textbox_style)
        self.textbox_teacher_specialization.setStyleSheet(textbox_style)
        self.textbox_teacher_name.setFixedWidth(300)
        self.textbox_teacher_bps.setFixedWidth(300)
        self.textbox_teacher_specialization.setFixedWidth(300)
        self.btn_add_teacher = QPushButton("Add Teacher")
        self.btn_add_teacher.setStyleSheet(button_style)
        self.btn_add_teacher.setFixedWidth(300)
        self.btn_add_teacher.clicked.connect(self.add_teacher)

        layout.addRow(self.label_teacher)
        layout.addRow(self.textbox_teacher_name)
        layout.addRow(self.textbox_teacher_bps)
        layout.addRow(self.textbox_teacher_specialization)
        layout.addRow("", self.btn_add_teacher)

        layout.setAlignment(self.label_teacher, Qt.AlignCenter)
        layout.setAlignment(self.textbox_teacher_name, Qt.AlignCenter)
        layout.setAlignment(self.textbox_teacher_bps, Qt.AlignCenter)
        layout.setAlignment(self.textbox_teacher_specialization, Qt.AlignCenter)
        layout.setAlignment(self.btn_add_teacher, Qt.AlignCenter)



        # Add the form layout to the container widget
        container_widget.setLayout(layout)

        # Add the container widget to the scroll area
        scroll_area.setWidget(container_widget)

        # Set the scroll area as the central widget of the window
        self.add_data_window.setCentralWidget(scroll_area)

        self.add_data_window.show()





        # These methods will be connected to the buttons
    def add_classroom(self):
        classroom_name = self.textbox_classroom.text()
        
        # Connect to the database
        connection = sqlite3.connect('timetable.db')
        cursor = connection.cursor()
        
        # Insert the new classroom name into the Classrooms table
        cursor.execute("""
            INSERT INTO Classrooms (classroom_name)
            VALUES (?)
        """, (classroom_name,))
        
        # Commit the changes and close the connection
        connection.commit()
        connection.close()
            # Display success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Classroom '{classroom_name}' added successfully!")
        msg.setWindowTitle("Success")
        msg.exec_()
        print(f"Classroom Added: {classroom_name}")
        self.textbox_classroom.setText("")


    def add_course(self):
        course_name = self.textbox_course_name.text()
        course_code = self.textbox_course_code.text()
        credits = self.textbox_course_credits.text()

        # Connect to the database
        connection = sqlite3.connect('timetable.db')
        cursor = connection.cursor()

        # Insert the new course data into the Courses table
        cursor.execute("""
            INSERT INTO Courses (course_name, course_code, credits)
            VALUES (?, ?, ?)
        """, (course_name, course_code, credits))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
    

        # Display success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Course '{course_name}' (Code: {course_code}, Credits: {credits}) added successfully!")
        msg.setWindowTitle("Success")
        msg.exec_()
    # Reset the text fields after successful insertion
        self.textbox_course_name.setText("")
        self.textbox_course_code.setText("")
        self.textbox_course_credits.setText("")
        print(f"Course Added: {course_name}, Code: {course_code}, Credits: {credits}")

    def add_day(self):
        # Get the selected day from the combobox
        day_name = self.combobox_day.currentText()

        # Connect to the database
        connection = sqlite3.connect('timetable.db')
        cursor = connection.cursor()

        # Insert the selected day into the Days table
        cursor.execute("""
            INSERT INTO Days (day_name)
            VALUES (?)
        """, (day_name,))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        # Display success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Day '{day_name}' added successfully!")
        msg.setWindowTitle("Success")
        msg.exec_()

        print(f"Day Added: {day_name}")

    def add_program(self):
        # Get the program name and semester from the textboxes
        program_name = self.textbox_program_name.text()
        semester = self.textbox_program_semester.text()

        # Connect to the database
        connection = sqlite3.connect('timetable.db')
        cursor = connection.cursor()

        # Insert the program data into the Programs table
        cursor.execute("""
            INSERT INTO Programs (program_name, semester)
            VALUES (?, ?)
        """, (program_name, semester))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        # Display success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Program '{program_name}' for Semester {semester} added successfully!")
        msg.setWindowTitle("Success")
        msg.exec_()

        # Reset the input fields
        self.textbox_program_name.clear()
        self.textbox_program_semester.clear()

        print(f"Program Added: {program_name}, Semester: {semester}")


    def add_teacher(self):
        # Get the teacher data from the textboxes
        teacher_name = self.textbox_teacher_name.text()
        bps_grade = self.textbox_teacher_bps.text()
        specialization = self.textbox_teacher_specialization.text()

        # Connect to the database
        connection = sqlite3.connect('timetable.db')
        cursor = connection.cursor()

        # Insert the teacher data into the Teachers table
        cursor.execute("""
            INSERT INTO Teachers (teacher_name, bps_grade, specialization)
            VALUES (?, ?, ?)
        """, (teacher_name, bps_grade, specialization))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        # Display success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Teacher '{teacher_name}' (BPS: {bps_grade}, Specialization: {specialization}) added successfully!")
        msg.setWindowTitle("Success")
        msg.exec_()

        # Reset the input fields
        self.textbox_teacher_name.clear()
        self.textbox_teacher_bps.clear()
        self.textbox_teacher_specialization.clear()

        print(f"Teacher Added: {teacher_name}, BPS: {bps_grade}, Specialization: {specialization}")

    def open_view_timetable_window(self):
        self.view_timetable_window = ViewTimetableWindow()  # Open the timetable window
        self.view_timetable_window.show()

    def open_update_data_window(self):
        self.update_data_window = MainWindow()  # Open the update data window
        self.update_data_window.show()

    def open_create_timetable_window(self):
        self.create_timetable_window = CreateTimetableWindow()  # Open the create timetable window
        self.create_timetable_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_app = MainApp()
    main_app.show()
    app.exec_()

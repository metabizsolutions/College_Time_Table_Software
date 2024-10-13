import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from AddData import AddDataWindow
from ViewTimetable import ViewTimetableWindow
from UpdateData import UpdateDataWindow
from CreateTimetable import CreateTimetableWindow
class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("College Timetable Management System")
        self.setGeometry(100, 100, 600, 500)  # Increased height for footer

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
        footer_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; padding: 10px;")
        self.layout.addWidget(footer_label)

    def open_add_data_window(self):
        self.add_data_window = AddDataWindow()
        self.add_data_window.show()

    def open_view_timetable_window(self):
        self.view_timetable_window = ViewTimetableWindow()  # Open the timetable window
        self.view_timetable_window.show()

    def open_update_data_window(self):
        self.update_data_window = UpdateDataWindow()  # Open the update data window
        self.update_data_window.show()

    def open_create_timetable_window(self):
        self.create_timetable_window = CreateTimetableWindow()  # Open the create timetable window
        self.create_timetable_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_app = MainApp()
    app.exec_()

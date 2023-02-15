from PyQt6.QtWidgets import QApplication, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QComboBox
from PyQt6.QtGui import QAction
import sqlite3
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Add a menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        about_menu_item = self.menuBar().addMenu("&Help")

        # Add submenu for menu bar
        file_menu_action = QAction("Add Student", self)
        file_menu_action.triggered.connect(self.insert)
        file_menu_item.addAction(file_menu_action)

        about_action = QAction("About", self)
        about_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Add a table structure
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id #", "Student Name", "Course", "Contacts"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Get data from database
    def load_data(self):
        # Connect to database
        connection = sqlite3.connect("database.db")
        # Get the table
        results = connection.execute("SELECT * FROM students")
        # Reset the table
        self.table.setRowCount(0)
        # Iterate through the tables to extract data
        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

        # Add insert method
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Details")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add contact widget
        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Contact")
        layout.addWidget(self.contact)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        contact = self.contact.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        # Add items to database
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, contact))

        connection.commit()
        cursor.close()
        connection.close()
        database.load_data()


app = QApplication(sys.argv)
database = MainWindow()
database.show()
database.load_data()
sys.exit(app.exec())

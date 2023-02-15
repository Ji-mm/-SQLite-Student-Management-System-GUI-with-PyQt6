from PyQt6.QtWidgets import QApplication, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sqlite3
import sys
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Add a menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        about_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add submenu for menu buttons
        add_student_action = QAction(QIcon("venv/icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_menu_item.addAction(about_action)

        search_action = QAction(QIcon("venv/icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Add a table structure
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id #", "Student Name", "Course", "Contacts"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create a status bar and elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

        # Get data from database

    def load_data(self):
        # Connect to database
        connection = sqlite3.connect("venv\database.db")
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

    # Add search method
    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def cell_clicked(self):
        # Add edit button
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        # Add delete button
        delete_button = QPushButton("Delete Record")
        edit_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Details")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # Display default student name
        index = database.table.currentRow()
        student_name = database.table.item(index, 1).text()
        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Get student ID
        self.student_ID = database.table.item(index, 0).text()

        # Add contact widget
        contact = database.table.item(index, 3).text()
        self.contact = QLineEdit(contact)
        self.contact.setPlaceholderText("Contact")
        layout.addWidget(self.contact)

        # Add combo box of courses
        course_name = database.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student_details)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student_details(self):
        connection = sqlite3.connect("venv\database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, "
                       "mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.contact.text(), self.student_ID))
        connection.commit()
        cursor.close()
        connection.close()
        # Refresh the table
        database.load_data()


class DeleteDialog(QDialog):
    pass


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
        connection = sqlite3.connect("venv\database.db")
        cursor = connection.cursor()
        # Add items to database
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, contact))

        connection.commit()
        cursor.close()
        connection.close()
        # Refresh the table
        database.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # Add search box widget
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # Add a submit button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.name.text()
        connection = sqlite3.connect("venv\database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)[0]
        items = database.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            database.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()
        database.load_data()


app = QApplication(sys.argv)
database = MainWindow()
database.show()
database.load_data()
sys.exit(app.exec())

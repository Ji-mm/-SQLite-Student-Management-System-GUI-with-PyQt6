from PyQt6.QtWidgets import QApplication, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem
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
        # Close connection
        connection.close()


app = QApplication(sys.argv)
database = MainWindow()
database.show()
database.load_data()
sys.exit(app.exec())

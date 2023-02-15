from PyQt6.QtWidgets import QApplication, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction

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
        self.setCentralWidget(self.table)



app = QApplication(sys.argv)
average_speed_calculator = MainWindow()
average_speed_calculator.show()
sys.exit(app.exec())

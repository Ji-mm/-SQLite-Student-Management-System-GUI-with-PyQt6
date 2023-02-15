from PyQt6.QtWidgets import QApplication, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow
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


app = QApplication(sys.argv)
average_speed_calculator = MainWindow()
average_speed_calculator.show()
sys.exit(app.exec())

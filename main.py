import sys
from PyQt6.QtWidgets import QApplication, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student management system")

        #creating a menubar
        file_menu_item = self.menuBar().addMenu("&File")
        help_manu_item = self.menuBar().addMenu("&Help")
        edit_menu_iem = self.menuBar().addMenu("&Edit")

        #Qaction for file:
        add_student_action = QAction("Add student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        #Qaction for help:
        about_action = QAction("About", self)
        help_manu_item.addAction(about_action)

        #Qaction for edit:
        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_iem.addAction(search_action)

        #creating a table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Phone no."))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    #function for loading the data into the table
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0) #to encounter add existing data
        for row_num, row_data in enumerate(result):
            # print(row_num, row_data)
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                # print(col_num,data)
                self.table.setItem(row_num,col_num, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


#new class for new window(insert window)
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert new student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.box = QComboBox(self)
        self.box.addItems(["Biology", "Math", "Astronomy", "Physics"])
        layout.addWidget(self.box)

        self.student_phone = QLineEdit()
        self.student_phone.setPlaceholderText("Phone no.")
        layout.addWidget(self.student_phone)

        btn = QPushButton("Insert data")
        btn.clicked.connect(self.add_student)
        layout.addWidget(btn)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.box.itemText(self.box.currentIndex())
        mobile = self.student_phone.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) Values (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        SMS.load_data()


#New class for new window (search)
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search for a student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        btn = QPushButton("Search")
        btn.clicked.connect(self.search)
        layout.addWidget(btn)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        coursor = connection.cursor()
        result = coursor.execute("SELECT * FROM students WHERE name = ?",
                                 (name,))
        rows = list(result)
        # print(rows)
        items = SMS.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            # print(item)
            SMS.table.item(item.row(), 1).setSelected(True)

        coursor.close()
        connection.close()


app = QApplication(sys.argv)
SMS = MainWindow()
SMS.show()
SMS.load_data()
sys.exit(app.exec())
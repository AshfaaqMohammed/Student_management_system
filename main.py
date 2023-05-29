import sys
from PyQt6.QtWidgets import QApplication, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, \
    QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student management system")
        self.setMinimumSize(800,600)

    # creating a menubar
        file_menu_item = self.menuBar().addMenu("&File")
        help_manu_item = self.menuBar().addMenu("&Help")
        edit_menu_iem = self.menuBar().addMenu("&Edit")

    # Qaction for file:
        add_student_action = QAction(QIcon("icons/add.png"),"Add student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

    # Qaction for help:
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_manu_item.addAction(about_action)


    # Qaction for edit:
        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_iem.addAction(search_action)

    # creating a table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Phone no."))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    # create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

    # create status bar an add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    # detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

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

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app is built using PYQT6 library, and sqlite3 as
        database.
        This app helps in managing the students , like inserting a new record
        or deleting a record or updating and also searching a record.
        """
        self.setText(content)


# New class for new window(delete window)
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete record")
        # self.setFixedWidth(250)
        # self.setFixedHeight(250)

        layout = QGridLayout()
        question = QLabel("Are you sure you want to delete?")
        yes = QPushButton("YES")
        no = QPushButton("NO")

        layout.addWidget(question, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        yes.clicked.connect(self.delete_student)

        self.setLayout(layout)

    def delete_student(self):
        index = SMS.table.currentRow()
        student_id = SMS.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        coursor = connection.cursor()
        coursor.execute("DELETE from students WHERE id = ?", (student_id, ))

        connection.commit()
        coursor.close()
        connection.close()
        SMS.load_data()

        self.close()

        conformation_widget = QMessageBox()
        conformation_widget.setWindowTitle("Success")
        conformation_widget.setText("The record was deleted successfully!")
        conformation_widget.exec()


# New class for new window(edit window)
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

    # getting student name from selected row
        index = SMS.table.currentRow()
        student_name = SMS.table.item(index, 1).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

    # getting student id
        self.student_id = SMS.table.item(index,0).text()

    # getting course name from selected row
        course_name = SMS.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

    # getting phone number from selected row
        phone_number = SMS.table.item(index, 3).text()
        self.student_number = QLineEdit(phone_number)
        self.student_number.setPlaceholderText("Phone no.")
        layout.addWidget(self.student_number)

    # Adding button
        btn = QPushButton("Update")
        btn.clicked.connect(self.update_record)
        layout.addWidget(btn)
        self.setLayout(layout)

    def update_record(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.student_number.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        # to refresh the table
        SMS.load_data()


# new class for new window(insert window)
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


# New class for new window (search)
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
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QPlainTextEdit, QMainWindow, QTextBrowser, \
    QDialog, QMenu, QAction, QMessageBox, QStatusBar, QSlider, QLabel, QCheckBox, QDialogButtonBox, QVBoxLayout, \
    QHBoxLayout, QScrollArea, QLineEdit, QTextEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import uic, QtGui
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import Qt
import resources
from copy import deepcopy,copy
from base import *
class AddTaskWindow(QDialog):
    def __init__(self):
        super(AddTaskWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/AddTaskWindow.ui'),self)
        self.NameField = self.findChild(QLineEdit,'NameField')
        self.DescriptionField = self.findChild(QTextEdit,'DescriptionField')
        self.buttonBox = self.findChild(QDialogButtonBox, 'buttonBox')

        self.buttonBox.accepted.connect(self.AddTaskToDb)
        self.buttonBox.rejected.connect(self.reject)

    def AddTaskToDb(self):
        nameText = self.NameField.text()
        descriptionText = self.DescriptionField.toPlainText()
        sql = "INSERT INTO tasks(name,description) VALUES('"+nameText+"','"+descriptionText+"');"
        cursor.execute(sql)
        db.commit()
class ViewEditTaskWindow(QDialog):
    def __init__(self):
        super(ViewEditTaskWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/ViewEditTaskWindow.ui'),self)
        self.NameField = self.findChild(QLineEdit,'NameField')
        self.DescriptionField = self.findChild(QTextEdit,'DescriptionFiled')

class AboutWindow(QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/AboutWindow.ui'),self)

class TaskBox(QCheckBox):
    def __init__(self):
        super(TaskBox, self).__init__()
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setStyleSheet(u"QCheckBox {\n"
                                   "    spacing: 5px;\n"
                                   "	background-color:rgb(0,0,0,0%);\n"
                                   "}\n"
                                   "\n"
                                   "QCheckBox::indicator {\n"
                                   "    width: 50px;\n"
                                   "    height: 50px;\n"
                                   "}\n"
                                   "\n"
                                   "QCheckBox::indicator:unchecked {\n"
                                   "    image: url(:/Resources/unchecked.png);\n"
                                   "}\n"
                                   "\n"
                                   "QCheckBox::indicator:unchecked:hover {\n"
                                   "    image: url(:/Resources/unchecked_hover.png);\n"
                                   "}\n"
                                   "\n"
                                   "QCheckBox::indicator:unchecked:pressed {\n"
                                   "    image: url(:/Resources/unchecked_pressed.png);\n"
                                   "}\n"
                                   "\n"
                                   "QCheckBox::indicator:checked {\n"
                                   "    image: url(:/Resources/checked.png);\n"
                                   "}\n"
                                   "\n"
                                   "QCheckBox::indicator:checked:hover {\n"
                                   "    image: url(:/Resources/checked_hover.png);\n"
                                   "}\n"
                                   "\n"
                                   "QCheckBox::indicator:checked:pressed {\n"
                                   "    image: url(:/Resources/checked_pressed.png);\n"
                                   "}\n"
                                   "\n"
                                   "")

class DetailsButton(QPushButton):
    def __init__(self):
        super(DetailsButton, self).__init__()
        self.setStyleSheet(u"QPushButton {\n"
                                       "	background-color:rgb(0,0,0,0%);\n"
                                       "	image: url(:/Resources/details.png);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:hover {\n"
                                       "    image: url(:/Resources/details_hover.png);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed {\n"
                                       "    image: url(:/Resources/details_clicked.png);\n"
                                       "}\n"
                                       "\n"
                                       "")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/TaskMainWindow.ui'),self)
        self.AboutAction = self.findChild(QAction,'actionAbout')
        self.ExitAction = self.findChild(QAction, 'actionExit')
        self.AddAction = self.findChild(QAction, 'actionAdd_Task')

        self.AboutAction.triggered.connect(self.ShowAbout)
        self.ExitAction.triggered.connect(self.close)
        self.AddAction.triggered.connect(self.ShowAddTask)
        # self.ScrollBoxContent = self.findChild(QVBoxLayout,'verticalLayout')
        # self.boxList =[]
        # self.num = "This is a Task This is a Task"
        # for i in range(10):
        #     self.Hlayout = QHBoxLayout()
        #     self.TaskBox = TaskBox()
        #     self.TaskBox.setText(self.num)
        #     self.TaskDetails = DetailsButton()
        #
        #     self.boxList.append((self.TaskBox,self.TaskDetails))
        #     self.Hlayout.addWidget(self.TaskBox)
        #     self.Hlayout.addWidget(self.TaskDetails,0, Qt.AlignLeft)
        #     self.ScrollBoxContent.addLayout(self.Hlayout)
        # print(self.boxList)

    def ShowAbout(self):
        self.about = AboutWindow()
        self.about.show()
        self.about.exec_()

    def ShowAddTask(self):
        self.addWindow = AddTaskWindow()
        self.addWindow.show()
        self.addWindow.exec_()

    def closeEvent(self, event):
        msg = QMessageBox()
        msg.setStyleSheet('color: white; background-color:#47515c; font-size:20px;')
        msg.setIcon(QMessageBox.Question)
        msg.setText("আপনি কি শিওর প্রস্থান করতে চান?")
        # msg.setInformativeText("এপ্লিকেশনটি চালাতে ইন্টারনেট সংযোগ প্রয়োজন")
        msg.setWindowTitle("Exit Warning")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ensure = msg.exec_()
        if ensure == QMessageBox.Yes:
            app = QApplication([])
            app.closeAllWindows()
            event.accept()
        else:
            event.ignore()



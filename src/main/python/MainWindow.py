from datetime import timedelta
from PyQt5.QtWidgets import QApplication, QDateEdit, QWidget, QPushButton, QProgressBar, QPlainTextEdit, QMainWindow, QTextBrowser, \
    QDialog, QMenu, QAction, QMessageBox, QStatusBar, QSlider, QLabel, QCheckBox, QDialogButtonBox, QVBoxLayout, \
    QHBoxLayout, QScrollArea, QLineEdit, QTextEdit, QSystemTrayIcon, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QEvent, QDate
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import resources
from base import *


class AddTaskWindow(QDialog):
    finished = pyqtSignal(tuple)
    def __init__(self):
        super(AddTaskWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/AddTaskWindow.ui'), self)
        self.NameField = self.findChild(QLineEdit, 'NameField')
        self.DescriptionField = self.findChild(QTextEdit, 'DescriptionField')
        self.buttonBox = self.findChild(QDialogButtonBox, 'buttonBox')
        self.deadline = self.findChild(QDateEdit,'deadline')
        self.noDeadline = self.findChild(QCheckBox,'noDeadline')

        self.buttonBox.accepted.connect(self.AddTaskToDb)
        self.buttonBox.rejected.connect(self.reject)

    def AddTaskToDb(self):
        nameText = self.NameField.text()
        descriptionText = self.DescriptionField.toPlainText()
        date = str(self.deadline.date().toPyDate())
        noDead = int(self.noDeadline.isChecked())
        # print(nameText,descriptionText,date,noDead)
        sql = f"INSERT INTO tasks(name,description,deadline,nodeadline,isdone)  VALUES('{nameText}','{descriptionText}','{date}','{noDead}',0);"
        cursor.execute(sql)
        db.commit()
        sql = "SELECT * FROM tasks ORDER BY ID DESC LIMIT 1;"
        cursor.execute(sql)
        row = cursor.fetchone()
        self.finished.emit(row)


class ViewEditTaskWindow(QDialog):
    finished = pyqtSignal(list)

    def __init__(self, id, index, isDone):
        super(ViewEditTaskWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/ViewEditTaskWindow.ui'), self)
        self.id = id
        self.ListIndex = index  # index of Box List
        self.isDone = isDone

        self.NameField = self.findChild(QLineEdit, 'NameField')
        self.DescriptionField = self.findChild(QTextEdit, 'DescriptionField')
        self.buttonBox = self.findChild(QDialogButtonBox, 'buttonBox')
        self.deadline = self.findChild(QDateEdit,'deadline')
        self.noDeadline = self.findChild(QCheckBox,'noDeadline')

        self.buttonBox.accepted.connect(self.EditTaskToDb)
        self.buttonBox.rejected.connect(self.reject)

    def EditTaskToDb(self):
        name = self.NameField.text()
        description = self.DescriptionField.toPlainText()
        date = str(self.deadline.date().toPyDate())
        noDead = int(self.noDeadline.isChecked())
        sql = "UPDATE tasks SET name ='" + name + \
              "',description='" + description + \
              "',deadline='" + date + \
              "',nodeadline='" + str(noDead) + \
              "' WHERE ID=" + str(self.id) + ";"
        cursor.execute(sql)
        db.commit()
        self.finished.emit([self.ListIndex, (self.id, name, description,date,noDead, self.isDone)])


class AboutWindow(QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/AboutWindow.ui'), self)


class TaskBox(QCheckBox):

    def __init__(self):
        super(TaskBox, self).__init__()
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        # self.setToolTip("Check and save to mark this task as completed")
        self.setStatusTip("Check and save to mark this task as completed")
        self.setStyleSheet(u"QCheckBox {\n"
                           "    spacing: 5px;\n"
                           "	background-color:rgba(0,0,0,0%);\n"
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
                           """QToolTip {
                                background-color: black;
                                color: white;
                                border: black solid 1px
                           }\n"""
                           "")


class DetailsButton(QPushButton):
    def __init__(self):
        super(DetailsButton, self).__init__()
        self.setToolTip("View/Edit task")
        self.setStatusTip("Click this button to view or edit this task")
        self.setStyleSheet(u"QPushButton {\n"
                           "	background-color:rgba(0,0,0,0%);\n"
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
                           """QToolTip {
                                background-color: black;
                                color: white;
                                border: black solid 1px
                           }\n"""
                           "")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(appContext.get_resource('ui/TaskMainWindow.ui'), self)
        self.fontDB = QtGui.QFontDatabase()
        self.fontID = self.fontDB.addApplicationFont(":Resources/BenSenHandwriting.ttf")
        self.font = QFont('BenSenHandwriting')
        QApplication.setFont(self.font)

        self.Tray = QSystemTrayIcon(self)
        self.Tray.setIcon(QIcon(":Resources/TaskReminder.png"))
        # self.TrayMenu = QMenu()
        # self.TrayMenu.addMenu("Exit")
        # self.TrayMenu.add
        self.Tray.activated.connect(self.__TrayOnclicked)
        self.Tray.setToolTip("Task Reminder")

        self.addWindow = None

        self.AboutAction = self.findChild(QAction, 'actionAbout')
        self.ExitAction = self.findChild(QAction, 'actionExit')
        self.AddAction = self.findChild(QAction, 'actionAdd_Task')
        self.importFile = self.findChild(QAction,'actionImport')
        self.Export = self.findChild(QAction,'actionExport')
        self.buttonBox = self.findChild(QDialogButtonBox,'buttonBox')

        self.AboutAction.triggered.connect(self.ShowAbout)
        self.ExitAction.triggered.connect(self.close)
        self.AddAction.triggered.connect(self.ShowAddTask)
        self.importFile.triggered.connect(self.ImportFile)
        self.Export.triggered.connect(self.ExportFile)
        self.buttonBox.accepted.connect(self.SaveTasks)
        self.buttonBox.rejected.connect(self.UndoComplete)

        self.TodayContent = self.findChild(QVBoxLayout, 'TodayLayout')
        self.WeekContent = self.findChild(QVBoxLayout, 'WeekLayout')
        self.UpcomingContent = self.findChild(QVBoxLayout, 'UpcomingLayout')
        self.MissedContent = self.findChild(QVBoxLayout, 'MissedLayout')
        self.DoneContent = self.findChild(QVBoxLayout, 'DoneLayout')

        self.Today = date.today()

        self.status_bar = self.findChild(QStatusBar,"statusbar")
        self.TaskList = []
        # self.result = self.FetchAllTask()
        # for row in self.result:
        #     self.AddTask(row)
        

        self.GetTodayList()
        self.GetWeekList()
        self.GetUpcomingList()
        self.GetMissedList()
        self.GetDoneList()
        # print(self.TaskList)
        self.AddButtonConnect()

    def GetTodayList(self):
        startdate = str(self.Today)
        # print(date)
        sql = f"SELECT * FROM tasks WHERE (deadline='{startdate}' OR nodeadline=1) AND isdone=0 ORDER BY id DESC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        for row in result:
            self.AddTask(row, self.TodayContent)

    def GetWeekList(self):
        startdate = str(self.Today+ timedelta(days=1))
        enddate = str(self.Today+ timedelta(days=7))
        # print(date)
        sql = f"SELECT * FROM tasks WHERE (deadline BETWEEN '{startdate}' AND '{enddate}') AND nodeadline=0 AND isdone=0 ORDER BY deadline ASC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        for row in result:
            self.AddTask(row, self.WeekContent)

    def GetUpcomingList(self):
        startdate = str(self.Today+ timedelta(days=7))
        # print(startdate)
        sql = f"SELECT * FROM tasks WHERE (deadline > '{startdate}') AND nodeadline=0 AND isdone=0 ORDER BY deadline ASC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        for row in result:
            self.AddTask(row, self.UpcomingContent)

    def GetMissedList(self):
        startdate = str(self.Today)
        # print(startdate)
        sql = f"SELECT * FROM tasks WHERE (deadline < '{startdate}') AND nodeadline=0 AND isdone=0 ORDER BY deadline DESC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        for row in result:
            self.AddTask(row, self.MissedContent)

    def GetDoneList(self):
        sql = f"SELECT * FROM tasks WHERE isdone=1 ORDER BY deadline DESC;"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        for row in result:
            self.AddTask(row, self.DoneContent, True)

    # def FetchAllTask(self):
    #     sql = "SELECT * FROM tasks"
    #     cursor.execute(sql)
    #     return cursor.fetchall()

    def AddTask(self, row, container, doneBox = False):
        name = row[1]
        self.Hlayout = QHBoxLayout()
        self.TaskBox = TaskBox()
        self.TaskBox.setText(name)
        if doneBox:
            self.TaskBox.setChecked(doneBox)
            self.TaskBox.setDisabled(doneBox)
        self.TaskDetails = DetailsButton()
        self.TaskList.append([row, self.TaskBox, self.TaskDetails])
        self.Hlayout.addWidget(self.TaskBox)
        self.Hlayout.addWidget(self.TaskDetails, 0, Qt.AlignLeft)
        container.addLayout(self.Hlayout)

    def AddButtonConnect(self):
        for i, task in enumerate(self.TaskList):
            task[2].clicked.connect(lambda *args, i=i, r=task: self.ShowViewTask(i, r))

    def ShowAbout(self):
        if hasattr(self,'about'):
            self.about.show()
            self.about.activateWindow()
        else:
            self.about = AboutWindow()
            self.about.show()
            self.about.exec_()


    def ShowAddTask(self):
        if self.addWindow is None:
            self.addWindow = AddTaskWindow()
            self.addWindow.finished.connect(self.UpdateTaskAfterAdd)
            self.addWindow.show()
            self.addWindow.exec_()
            self.addWindow = None
        else:
            self.addWindow.activateWindow()


    def ShowViewTask(self, index, task):
        # print(task)
        row, nameField, desField = task
        self.ViewWindow = ViewEditTaskWindow(row[0], index, row[5])
        self.ViewWindow.NameField.setText(row[1])
        self.ViewWindow.DescriptionField.setPlainText(row[2])
        Deadline = list(map(int, row[3].strip().split('-')))
        self.ViewWindow.deadline.setDate(QDate(Deadline[0],Deadline[1],Deadline[2]))
        self.ViewWindow.noDeadline.setChecked(bool(row[4]))
        self.ViewWindow.finished.connect(self.UpdateTask)
        self.ViewWindow.finished.connect(self.ViewWindow.close)
        self.ViewWindow.show()

    def UpdateTask(self, list):
        index = list[0]
        row = list[1]
        self.status_bar.showMessage(f"Updated task <<{row[1]}>> successfully.")
        # self.TaskList[index][0] = row  # updated row of list
        # self.TaskList[index][1].setText(row[1])  # updated taskbox text
        # self.TaskList[index][2].clicked.connect(lambda *args, i=index, r=self.TaskList[index]: self.ShowViewTask(i, r))
        # self.result = self.FetchAllTask()
        self.Refresh()

    def UpdateTaskAfterAdd(self, row):
        self.status_bar.showMessage(f"Added task <<{row[1]}>> successfully.")
        if row[4] == 1 or (datetime.strptime(row[3],r"%Y-%m-%d").date() == self.Today):
            container = self.TodayContent
        elif 1<= (datetime.strptime(row[3],r"%Y-%m-%d").date()-self.Today).days <= 7:
            container = self.WeekContent
        elif (datetime.strptime(row[3],r"%Y-%m-%d").date()-self.Today).days > 7:
            container = self.UpcomingContent
        else:
            container = self.MissedContent

        self.AddTask(row,container)
        # self.AddButtonConnect()
        self.TaskList[-1][2].clicked.connect(lambda *args, i=len(self.TaskList)-1, r=self.TaskList[-1]: self.ShowViewTask(i, r))

    def SaveTasks(self):
        msg = QMessageBox()
        msg.setStyleSheet('color: white; background-color:#47515c; font-size:20px;')
        msg.setIcon(QMessageBox.Question)
        msg.setText("Are you sure the tasks have been completed?")
        msg.setWindowTitle("Save & Exit Warning")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ensure = msg.exec_()
        if ensure == QMessageBox.Yes:
            for task in self.TaskList:
                ID = task[0][0]
                if task[1].isChecked():
                    # sql = "DELETE FROM tasks WHERE ID=" + str(ID) + ";"
                    sql = "UPDATE tasks SET isdone = 1 WHERE ID=" + str(ID) + ";"
                    cursor.execute(sql)
            db.commit()
            self.status_bar.showMessage("All changes saved, waiting for the system to exit...")
            app = QApplication([])
            app.closeAllWindows()
        else:
            # event.ignore()
            pass

    def UndoComplete(self):
        for task in self.TaskList:
            if task[1].isChecked():
                task[1].setChecked(False)

    def Refresh(self):
        self.deleteLayout(self.TodayContent)
        self.deleteLayout(self.WeekContent)
        self.deleteLayout(self.UpcomingContent)
        self.deleteLayout(self.MissedContent)
        self.deleteLayout(self.DoneContent)
        self.TaskList =[]

        self.GetTodayList()
        self.GetWeekList()
        self.GetUpcomingList()
        self.GetMissedList()
        self.GetDoneList()

        self.AddButtonConnect()

    def deleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            # sip.delete(layout)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState()==Qt.WindowMinimized:
                self.hide()
                self.Tray.show()
            elif self.windowState()==Qt.WindowMaximized:
                self.showMaximized()

    def closeEvent(self, event):
        msg = QMessageBox()
        msg.setStyleSheet('color: white; background-color:#47515c; font-size:20px;')
        msg.setIcon(QMessageBox.Question)
        msg.setText("Are you sure you want to exit?")
        msg.setWindowTitle("Exit Warning")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ensure = msg.exec_()
        if ensure == QMessageBox.Yes:
            app = QApplication([])
            app.closeAllWindows()
            event.accept()
        else:
            event.ignore()

    def __TrayOnclicked(self,reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.activateWindow()
            self.showNormal()
            self.Tray.hide()

    def ImportFile(self):
        file = QFileDialog.getOpenFileName(caption='Import Existing Data',directory=desktop,filter="Task Reminder File(*.koly)")
        file_name = file[0]
        if file_name !='':
            #need to work on exception handling later
            with open(file_name,'rb') as k: 
                data = k.read()
                with open(db_dir+r"/Task.db",'wb') as f:
                    f.write(data)
                    self.Refresh()

    def ExportFile(self):
        file = QFileDialog.getSaveFileName(caption='Export All Data',directory=desktop,filter="Task Reminder File(*.koly)")
        file_name = file[0]
        if file_name !='':
            #need to work on exception handling later
            with open(db_dir+r"/Task.db",'rb') as f:
                data = f.read()
                with open(file_name,'wb') as k:
                    k.write(data)

class DupicateInstance():
    def __init__(self):
        msg = QMessageBox()
        msg.setStyleSheet('color: white; background-color:#47515c; font-size:20px;')
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Application is running already ")
        msg.setWindowTitle("Duplicate Instance Warning")
        msg.setStandardButtons(QMessageBox.Abort)
        ensure = msg.exec_()
        if ensure == QMessageBox.Abort:
            app = QApplication([])
            app.closeAllWindows()


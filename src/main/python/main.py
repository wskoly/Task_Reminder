from base import *
from MainWindow import MainWindow, DupicateInstance
import psutil

if __name__ == '__main__':
    proccess_list= [i.name() for i in psutil.process_iter()]
    p_count = proccess_list.count("Task Reminder.exe")
    if p_count<2:
        window = MainWindow()
        window.show()
    else:
        duplicate = DupicateInstance()
    exit_code = appContext.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
from base import *
from MainWindow import MainWindow

if __name__ == '__main__':
    window = MainWindow()
    window.show()
    exit_code = appContext.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
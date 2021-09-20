from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import sqlite3
import os
from datetime import date, timedelta, datetime

app_data = os.getenv('APPDATA')
db_dir = os.path.join(app_data, "KOLY- Task Reminder\Database")
db_file = db_dir+r"/Task.db"
desktop = os.path.expanduser('~\Desktop')
if not os.path.exists(db_dir+r"/Task.db"):
    try:
        os.makedirs(db_dir)
    except:
        pass
    #need to work on exception handling later
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    sql = """CREATE TABLE tasks
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name CHAR(50) NOT NULL,
            Description TEXT NOT NULL,
            Deadline DATE,
            NoDeadline INTEGER NOT NULL,
            IsDone INTEGER NOT NULL);"""
    cursor.execute(sql)
else:
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
appContext = ApplicationContext()
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import sqlite3
import os

app_data = os.getenv('APPDATA')
db_dir = os.path.join(app_data, "Task Reminder\Database")
db_file = db_dir+r"/Task.db"
if not os.path.exists(db_dir+r"/Task.db"):
    try:
        os.makedirs(db_dir)
    except:
        pass
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    sql = """CREATE TABLE tasks
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name CHAR(50) NOT NULL,
            Description TEXT NOT NULL);"""
    cursor.execute(sql)
else:
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
appContext = ApplicationContext()
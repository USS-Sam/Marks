import sqlite3
connection = sqlite3.connect ("marks.db")
cursor = connection.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS CSS(
       SNo INTEGER PRIMARY KEY AUTOINCREMENT,
       RollNo INTEGER,
       Name TEXT,
       Mobile INTEGER,
       Marks INTEGER)'''
)
connection.commit()
connection.close()
print("Database storage is ready!")
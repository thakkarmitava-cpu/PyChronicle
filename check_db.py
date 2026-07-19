# 
import sqlite3

conn = sqlite3.connect("database/pychronicle.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM runtime_log")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
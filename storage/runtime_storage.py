import sqlite3


class RuntimeStorage:

    def __init__(self):
        self.conn = sqlite3.connect("database/pychronicle.db")
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS runtime_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            line INTEGER,
            function TEXT,
            variables TEXT
        )
        """)
        self.conn.commit()

    def insert_runtime(self, line, function, variables):
        self.cursor.execute("""
        INSERT INTO runtime_log(line,function,variables)
        VALUES(?,?,?)
        """, (line, function, str(variables)))

        self.conn.commit()
    def clear_table(self):
     self.cursor.execute("DELETE FROM runtime_log")
     self.conn.commit()    
    
    def get_all_runtime(self):
     self.cursor.execute("""
        SELECT line, function, variables
        FROM runtime_log
        ORDER BY id
    """)
     return self.cursor.fetchall()
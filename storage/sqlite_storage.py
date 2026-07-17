import sqlite3


class Storage:

    def __init__(self):
        self.connection = sqlite3.connect("database/pychronicle.db")
        self.cursor = self.connection.cursor()

        print("Database Connected")

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS variable_log (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            variable_name TEXT,

            line_number INTEGER,

            type TEXT
        )
        """)

        self.connection.commit()

        print("Table Created")

    def clear_table(self):
        self.cursor.execute("DELETE FROM variable_log")
        self.connection.commit()

    def insert_variable(self, variable):
        self.cursor.execute("""
        INSERT INTO variable_log
        (variable_name, line_number, type)
        VALUES (?, ?, ?)
        """, (
            variable["variable"],
            variable["line"],
            variable["type"]
        ))

        self.connection.commit()

    def get_all_variables(self):
        self.cursor.execute("SELECT * FROM variable_log")
        return self.cursor.fetchall()
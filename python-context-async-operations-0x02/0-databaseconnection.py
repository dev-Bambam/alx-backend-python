"""

Objective: create a class based context manager to handle opening and closing database connections automatically

Instructions:

Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.

"""

import sqlite3
class DbConnection:
    def __init__(self, file_path):
        self.file_path = file_path
                 
    def __enter__(self):
        self.connection = sqlite3.connect(self.file_path)
        return self.connection

    def __exit__(self, exec_type, exec_value, traceback):
        self.connection.close()


with DbConnection('./users.db') as conn:
    cursor = conn.cursor()
    cursor.execute('select * from users')
    users = cursor.fetchall()
    print(f'users: {users}')


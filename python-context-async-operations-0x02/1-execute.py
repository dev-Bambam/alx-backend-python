"""

Objective: create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution

Instructions:

Implement a class based custom context manager ExecuteQuery that takes the query: ”SELECT * FROM users WHERE age > ?” and the parameter 25 and returns the result of the query

Ensure to use the __enter__() and the __exit__() methods

"""
import sqlite3


class ExecuteQuery:
    def __init__(self, query, file_path, parameter):
        self.file_path = file_path,
        self.connection = None
        self.query = query
        self.parameter = parameter

        print(f'file_path:{self.file_path}\n query:{self.query}\n parameter:{self.parameter}')
        
    def __enter__(self):
        self.connection = sqlite3.connect(self.file_path)
        cursor = self.connection.cursor()
        cursor.execute(self.query, (self.parameter,))
        result = cursor.fetchall()

        return  result
    
    def __exit__(self, exec_type, exec_value, traceback):
        if self.connection:
            self.connection.close()
        else:
            return False
        
with ExecuteQuery(
    "select * from users where age > ?", "./users.db", 25
) as result:
    print(f'result:{result}')
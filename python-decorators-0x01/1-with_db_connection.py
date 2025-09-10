"""

Objective: create a decorator that automatically handles opening and closing database connections

Instructions:

Complete the script below by Implementing a decorator with_db_connection that opens a database connection, passes it to the function and closes it afterword

"""

import sqlite3
import os

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        db_path = os.path.join(os.getcwd(), 'db', 'users.db')
        try:
            with sqlite3.connect(db_path) as conn:
                args = (conn,) + args
                result = func(*args, **kwargs)
        except sqlite3.Error as e:
            print(f'error: {e}')
            result = []
        return result

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id, ))
    return cursor.fetchone()

user = get_user_by_id(user_id=1)
print(user)
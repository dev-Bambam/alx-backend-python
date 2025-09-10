"""
Objective: create a decorator that logs database queries executed by any function

Instructions:

Complete the code below by writing a decorator log_queries that logs the SQL query before executing it.

Prototype: def log_queries()

"""

import sqlite3
import os

# decorator to log sql queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        print(f'query: {args[0] if args else 'No query'}')
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    db_path = os.path.join(os.getcwd(), 'db', 'user.db')
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f'error: {e}')
        result = []
    return result


users = fetch_all_users('SELECT * FROM users')
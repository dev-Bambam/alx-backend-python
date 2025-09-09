'''
# Ok so I just learnt about decorator in python and it's really great, it's a great way of modifying the behavior of a function without changing the function's functionality itself. a decorator is a function that takes a function as an arg and return the function, the function the decorator take as an argument is the function/methods we want to decorate, then the decorator adds a wrapper function around the function which will have acess to the args of the function/methods that needs to be decorated, we return the decorator arg from the wrapper func so that the function can run and we return the wrapper as a variable.

# ok so learnt about context manager using it to handle db connection, using context manager I don't need to worry about closing the connection once I am done

# also using os to work with file path instead of me using hardcoded code
'''

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
"""

Objective: create a decorator that retries database operations if they fail due to transient errors

Instructions:

Complete the script below by implementing a retry_on_failure(retries=3, delay=2) decorator that retries the function of a certain number of times if it raises an exception

What are Transient Error:

This means temporary, non-fatal errors that are likely to disappear on their own after a short time.

Example Transient Errors:

- A brief network interruption.
- A database server that is temporarily overloaded.
- A timeout waiting for a response.

Example Permanent Errors:

- A syntax error in your SQL query.
- Trying to connect to a database that doesn't exist.

"""

import sqlite3
import os
import time

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        db_path = os.path.join(os.getcwd(), 'db', 'users.db')
        with sqlite3.connect(db_path) as conn:
            return func(conn, *args, **kwargs)
        
    return wrapper


def retry_on_failure(retries, delay):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except sqlite3.Error as e:
                    if attempt == retries:
                        print(f'Attempt {attempt} failed. Max retries exceeded.')
                        print(f'{e}')
                        # raise
                    else:
                        print(f'Attempt {attempt} failed, Retrying in {delay}s')
                        time.sleep(delay)
        return wrapper
    return decorator

                    

@with_db_connection
@retry_on_failure(retries=4, delay=3)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

users = fetch_users_with_retry()
print(f'Users: {users}')
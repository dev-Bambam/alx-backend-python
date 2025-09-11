"""

Objective: create a decorator that caches the results of a database queries inorder to avoid redundant calls

Instructions:

Complete the code below by implementing a decorator cache_query(func) that caches query results based on the SQL query string

"""

import sqlite3
import os


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        db_path = os.path.join(os.getcwd(), "db", "users.db")
        with sqlite3.connect(db_path) as conn:
            return func(conn, *args, **kwargs)

    return wrapper


# @with_db_connection
# def create_table(conn):
#     try: 
#         cursor = conn.cursor()
#         cursor.execute(
#         '''
#             CREATE TABLE users(
#                 id INTEGER PRIMARY KEY,
#                 first_name VARCHAR(50) NOT NULL,
#                 last_name VARCHAR(50) NOT NULL,
#                 email UNIQUE NOT NULL
#             )
#         '''
#         )
#     except sqlite3.Error as e:
#         print(f'DB_Error: {e}')
#     else:
#         print('table created successfully')



def cache_query(func):
    cache = {}
    def wrapper(*args, **kwargs):
        cache_key  = kwargs['query']
        if cache_key in cache:
            print('printed from cache')
            return cache[cache_key]
        else:
            result = func(*args, **kwargs)
            cache[cache_key] = result

        return result
        
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# first call will catch the result
users = fetch_users_with_cache_query(query="SELECT * FROM users")


# second call will use the cache instead of querying the DB
users_again = fetch_users_with_cache_query(query="SELECT * FROM users")

print(f"first user call: {users}\n")
print(f"second user call: {users_again}\n")
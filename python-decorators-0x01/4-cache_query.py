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


# my initial implementation

# def cache_query(func):
#     cache = {}
#     def wrapper(*args, **kwargs):
#         cache_key  = kwargs['query']
#         if cache_key in cache:
#             return cache[cache_key]
#         else:
#             result = func(*args, **kwargs)
#             cache[cache_key] = result

#         return result
        
#     return wrapper

def cache_query(func):
    cache = {} # this create a global cache for all function
    cache.setdefault(func.__name__, {}) # this set each unique func call as a key which the value is a {} which contain the different args and kwargs of the func as the key and the result of the function call

    def wrapper(*args, **kwargs):
        query_args = args[1:]  # line 45 and 46 makes both args/kwargs a unique key by converting them to tuples and sorting the kwargs so that the order of the kwargs doesn't matter so far they are the same
        cache_key = (query_args, tuple(sorted(kwargs.items())))

        if cache_key in cache:
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

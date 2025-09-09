'''
Ok so I just learnt about decorator in python and it's really great, it's a great way of modifying the behavior of a function without changing the function's functionality itself. a decorator is a function that takes a function as an arg and return the function, the function the decorator take as an argument is the function/methods we want to decorate, then the decorator adds a wrapper function around the function which will have acess to the args of the function/methods that needs to be decorated, we return the decorator arg from the wrapper func so that the function can run and we return the wrapper as a variable.
'''

import sqlite3



# decorator to log sql queries
def log_queries(func):
    def wrapper(query):
        print(f'query: {query}')
        return func(query)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    return result

users = fetch_all_users('SELECT * FROM users')

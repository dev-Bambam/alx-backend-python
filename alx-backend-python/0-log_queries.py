import sqlite3



# decorator to log sql queries
def log_queries(func):
    def wrapper(query):
        print(f'query:{query}')
        return func(query)
    
    return wrapper()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    return result

users = fetch_all_users('SELECT * FROM users')

    

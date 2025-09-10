import sqlite3
import os

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        db_path = os.path.join(os.getcwd(), 'db', 'user.db')
        try:
            with sqlite3.connect(db_path) as conn:
                args = (conn,) + args
                result = func(*args, **kwargs)
        except sqlite3.Error as e:
            return e
        return result
    
    return wrapper

def transactional(func):
    def wrapper(*args, **kwargs):
        conn = args[0]
        try:
             func(*args, **kwargs)
        except Exception as e:
            conn.rollback()
            print(f'Error Occured during transaction:{e}')
        else:
            conn.commit()

    return wrapper



@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email=? WHERE id=?", (new_email, user_id))

result = update_user_email(user_id=1, new_email='ay@gmail.com')
print(f'result coming from the last print: {(result)}')
    
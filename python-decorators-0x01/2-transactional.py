import sqlite3
import os


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        db_path = os.path.join(os.getcwd(), "db", "user.db")
        with sqlite3.connect(db_path) as conn:
            args = (conn,) + args
            return func( *args, **kwargs)
        

    return wrapper


def transactional(func):
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error Occured during transaction:{e}")
            raise
        else:
            conn.commit()
            return result

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email=? WHERE id=?", (new_email, user_id))


result = update_user_email(user_id=1, new_email="ay@gmail.com")
print(f"result coming from the last print: {(result)}")

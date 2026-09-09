import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

conn.commit()  

def register_user(username, password, role="user"):

    try:

        cursor.execute(
            """
            INSERT INTO users(username, password, role)
            VALUES(?,?,?)
            """,
            (username, password, role)
        )

        conn.commit()

        return True

    except Exception:

        return False
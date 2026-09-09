from database import cursor, conn
from auth import hash_password

username = "admin"
password = hash_password("admin123")

cursor.execute(
    "INSERT OR IGNORE INTO users(username,password,role) VALUES(?,?,?)",
    (
        username,
        password,
        "admin"
    )
)

conn.commit()

print("Admin Created")
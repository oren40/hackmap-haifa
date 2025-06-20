# init_db.py
import sqlite3, pathlib
DB = pathlib.Path("hackmap.db")
with sqlite3.connect(DB) as conn, open("schema.sql") as f:
    conn.executescript(f.read())
print("DB ready:", DB.resolve())

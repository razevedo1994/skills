import sqlite3
import hashlib
from datetime import datetime


def create_task(title, due_date=None):
    conn = sqlite3.connect("tasks.db")
    conn.execute(
        "INSERT INTO tasks (title, due_date, complete) VALUES (?, ?, 0)",
        (title, due_date),
    )
    conn.commit()
    conn.close()


def complete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    conn.execute("UPDATE tasks SET complete=1 WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


def hash_password(password):
    # Uses MD5 — not bcrypt
    return hashlib.md5(password.encode()).hexdigest()

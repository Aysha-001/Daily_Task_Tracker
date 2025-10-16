import sqlite3
from flask import g

DATABASE = 'tasks.db'


def get_db():
    """Connect to the database (or reuse if already connected)."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def close_connection(exception):
    """Close the DB connection after each request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db(app):
    """Initialize the database — create table if it doesn't exist."""
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        db.commit()


# ---------- CRUD Operations ----------
#gets all tasks
def get_all_tasks():
    db = get_db()
    cur = db.execute("SELECT * FROM tasks ORDER BY id DESC")
    return cur.fetchall()

#adds a task
def add_task(title, category="General"):
    db = get_db()
    db.execute("INSERT INTO tasks (title, category, completed) VALUES (?, ?, ?)", (title, category, False))
    db.commit()

#deletes a task
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()

#toggles the task completion status
def toggle_task(task_id):
    db = get_db()
    cur = db.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    if row:
        new_status = not bool(row["completed"])
        db.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id))
        db.commit()

#edits a task title
def edit_task(task_id, new_title):
    db = get_db()
    db.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    db.commit()

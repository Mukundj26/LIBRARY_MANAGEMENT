import sqlite3
from flask import g
from config import Config


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(Config.DATABASE_PATH)
        db.row_factory = sqlite3.Row
        # Enable foreign key support
        db.execute("PRAGMA foreign_keys = ON")
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    last_id = cur.lastrowid
    db.commit()
    cur.close()
    return last_id


def log_activity(action_type, target_table, user_name, description):
    """Log a system action to the system_logs table."""
    query = "INSERT INTO system_logs (action_type, target_table, user_name, description) VALUES (?, ?, ?, ?)"
    execute_db(query, [action_type, target_table, user_name, description])


def init_db(app):
    """Create database file and run schema."""
    import os
    db_dir = os.path.dirname(Config.DATABASE_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    with app.app_context():
        db = get_db()
        with app.open_resource('database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

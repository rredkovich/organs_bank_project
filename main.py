import sqlite3
from app.app import Demo
from db import initialise_db

def initialise_from_scratch(conn):
    initialise_db.create_tables(conn)
    initialise_db.prefill_lib_data(conn)


if __name__ == '__main__':
    db_name = 'dev.db'
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")

    app = Demo(conn)
    app.run()
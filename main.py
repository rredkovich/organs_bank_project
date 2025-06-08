import sqlite3
from app.app import App
from db import initialise_db
from settings import db_connection

def initialise_from_scratch(conn):
    initialise_db.create_tables(conn)
    initialise_db.prefill_lib_data(conn)



if __name__ == '__main__':
    # initialise_from_scratch(db_connection)
    app = App()
    app.run()
import sqlite3
from db import initialise_db

db_name = 'dev.db'

conn = sqlite3.connect(db_name)

initialise_db.create_tables(conn)
initialise_db.prefill_lib_data(conn)


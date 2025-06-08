import sqlite3


db_name = "clean_application_db.sqlite"
# db_name = "application_db.sqlite"

db_connection = sqlite3.connect(db_name)
db_connection.execute("PRAGMA foreign_keys = ON")


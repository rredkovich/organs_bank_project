import sqlite3
import settings

conn = sqlite3.connect(settings.database_fname)
db_curr = conn.cursor()


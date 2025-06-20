"""
Fills up known in advance system data
"""
import sqlite3
from . import schema

# https://en.wikipedia.org/wiki/Transplantable_organs_and_tissues
transplantable_organs = (
    'heart',
    'lung',
    'kidney',
    'liver',
    'pancreas',
    'intestine',
    'cornea',
    'skin',
    'blood',
    'blood plasma',
    'heart valve',
)

# https://en.wikipedia.org/wiki/Blood_transfusion
blood_types = (
    "AB+",
    "AB-",
    "A+",
    "A-",
    "B+",
    "B-",
    "O+",
    "O-",
)

genders = (
    "male",
    "female",
)

def create_tables(conn: sqlite3.Connection):
    cur = conn.cursor()
    for table in schema.all_tables:
        cur.execute(table)
    conn.commit()

def prefill_lib_data(conn: sqlite3.Connection):
    """Prefils library data"""
    cur = conn.cursor()
    for gender in genders:
        cur.execute(f"insert into genders (gender) values ('{gender}');")

    for blood_type in blood_types:
        cur.execute(f"insert into blood_types (blood_type) values ('{blood_type}');")

    for organ_name in transplantable_organs:
        cur.execute(f"insert into organ_names (organ_name) values ('{organ_name}');")

    conn.commit()

def init_db( conn: sqlite3.Connection):
    """Creates all tables and prefill the base libraries data"""
    create_tables(conn)
    prefill_lib_data(conn)
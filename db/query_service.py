"""
CRUD Operations
"""
import sqlite3
from . import utilities
from dataclasses import fields
from typing import List, Tuple, Any
# TODO: put primary_key_by_class utility function to other module and move its call from query service? possible leaking
# abstraction to call it from here
from db.utilities import primary_key_by_class


class QueryService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def execute(self, query: str):
        cur = self.db.cursor()
        cur.execute(query)
        cur.fetchall()

    def _prepare_dataclass(self, dc: "BaseDT") -> Tuple[str, Tuple[str], Tuple[Any]]:
        """Prepares basic SQL info from a dataclass,
        return table name, tuple of field names, tuple of corresponding values"""
        table_name = utilities.class_to_table_name(dc.__class__.__name__)
        field_names = fields(dc)
        columns = tuple(f.name for f in field_names)
        values = tuple(getattr(dc, f.name) for f in field_names)
        return table_name, columns, values

    def _prepare_insert_stmt(self, dc: "BaseDT") -> Tuple[str, Tuple[Any]]:
        """Creates INSERT SQL statement, returns the statement and values"""
        table_name, columns, values = self._prepare_dataclass(dc)

        # As we rely on autocreated by DB IDs dropping the first col/val if it's entity 'id'
        if columns[0] == primary_key_by_class(dc.__class__):
            columns, values = columns[1:], values[1:]
        placeholders = ', '.join('?' for _ in values)
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) RETURNING *"
        return sql, values

    def _prepare_update_stmt(self, dc: "BaseDT") -> Tuple[str, Tuple[Any], Tuple[Any]]:
        """Creates UPDATE SQL statement, returns the statement and values"""
        # DB structure assume that first column is either id (PK / FK) or it is library table
        # where text value is also PK
        table_name, columns, values = self._prepare_dataclass(dc)
        value_columns = columns if len(columns) == 1 else columns[1:]
        values = values if len(values) == 1 else values[1:] + (values[0],)
        cols_with_placeholders = ', '.join(f"{column} = ?" for column in value_columns)
        cols = [f.name for f in fields(dc)]
        sql = f"UPDATE {table_name} SET {cols_with_placeholders} WHERE {columns[0]} = ? RETURNING {", ".join(cols)}"
        return sql, values

    def _prepare_delete_stmt(self, dc: "BaseDT") -> Tuple[str, Tuple[Any]]:
        """Creates DELETE SQL statement, returns the statement and values"""
        table_name, columns, values = self._prepare_dataclass(dc)
        if columns[0] != primary_key_by_class(dc.__class__):
            raise ValueError("Attempt to delete non-pk column, are you trying to remove library value?..")
        sql = f"DELETE FROM {table_name} WHERE {columns[0]} = ?"
        return sql, (values[0],)

    def create(self, dc: "BaseDT") -> "BaseDT":
        "Creates new DB record of given object, auto-sets its ID"
        stmt, values = self._prepare_insert_stmt(dc)
        cursor = self.conn.cursor()
        cursor.execute(stmt, values)
        inserted = cursor.fetchone()
        cols = [f.name for f in fields(dc) if f.name.endswith("_id")]

        setattr(dc, cols[0], inserted[0])
        self.conn.commit()
        return dc

    def update(self, dc: "BaseDT") -> "BaseDT":
        """Updates DB record with provided data. Replaces all data in row with it! Except *id columns of course"""
        stmt, values = self._prepare_update_stmt(dc)
        cursor = self.conn.cursor()
        cursor.execute(stmt, values)
        updated = cursor.fetchone()
        self.conn.commit()

    def fetch_one(self, id: int, klass: "BaseDT") -> "BaseDT":
        """Fetches DB record from a table which corresponds to the klass by provided id,
        returns the instance of the klass"""
        table_name = utilities.class_to_table_name(klass.__name__)
        cols = [f.name for f in fields(klass)]
        pk_col = primary_key_by_class(klass)

        stmt = f"SELECT {', '.join(cols)} FROM {table_name} WHERE {pk_col} = ?"

        cursor = self.conn.cursor()
        cursor.execute(stmt, (id,))
        fetched = cursor.fetchone()
        return klass(*fetched)

    def fetch_filtered(self, filter_field: str, value: Any, klass: "BaseDT") -> List["BaseDT"]:
        """Fetches DB records from a table which corresponds to the klass by provided field's value,
        returns the list of instances of the klass."""
        table_name = utilities.class_to_table_name(klass.__name__)
        cols = [f.name for f in fields(klass)]
        stmt = f"SELECT {", ".join(cols)} FROM {table_name} WHERE {filter_field} = ? ORDER BY created_at ASC"
        cursor = self.conn.cursor()
        cursor.execute(stmt, (value, ))
        fetched = cursor.fetchall()
        return [klass(*row) for row in fetched]

    def fetch_all(self, klass: "BaseDT") -> List["BaseDT"]:
        """Fetches all records from the table which corresponds to the klass.
        Returns the list of instances of the klass."""
        table_name = utilities.class_to_table_name(klass.__name__)
        cols = [f.name for f in fields(klass)]
        stmt = f"SELECT {", ".join(cols)} FROM {table_name} ORDER BY created_at ASC"
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        fetched = cursor.fetchall()
        objs = [klass(*row) for row in fetched]
        return objs

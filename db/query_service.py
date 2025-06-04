"""
CRUD Operations
"""
import sqlite3
from . import utilities
from dataclasses import fields
from typing import List, Tuple, Any


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
        # As we rely on autocreated by DB IDs dropping the first col/val if it's 'id'
        if columns[0] == 'id':
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
        sql = f"UPDATE {table_name} SET {cols_with_placeholders} WHERE {columns[0]} = ? RETURNING *"
        return sql, values

    def _prepare_delete_stmt(self, dc: "BaseDT") -> Tuple[str, Tuple[Any]]:
        """Creates DELETE SQL statement, returns the statement and values"""
        table_name, columns, values = self._prepare_dataclass(dc)
        if not columns[0].endswith('id'):
            raise ValueError("Attempt to delete non-id column, are you trying to remove library value?..")
        sql = f"DELETE FROM {table_name} WHERE {columns[0]} = ?"
        return sql, (values[0],)

    def create(self, dc: "BaseDT") -> "BaseDT":
        "Creates new DB record of given object, auto-sets its ID"
        stmt, values = self._prepare_insert_stmt(dc)
        cursor = self.conn.cursor()
        cursor.execute(stmt, values)
        inserted = cursor.fetchone()

        dc.id = inserted[0]
        self.conn.commit()
        return dc

    def update(self, dc: "BaseDT") -> "BaseDT":
        """Updates DB record with provided data. Replaces all data in row with it! Except *id columns of course"""
        stmt, values = self._prepare_update_stmt(dc)
        cursor = self.conn.cursor()
        cursor.execute(stmt, values)
        updated = cursor.fetchone()
        self.conn.commit()


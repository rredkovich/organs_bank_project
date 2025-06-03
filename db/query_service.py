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
        placeholders = ', '.join('?' for _ in values)
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, columns, placeholders)
        return sql, values

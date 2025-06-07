from typing import List, Tuple
from db.query_service import QueryService
from db import models as db
from db.utilities import data_class_fields_names
from settings import db_connection


class BaseModel:
    def __init__(self, klass: "BaseDS"):
        self.qs = QueryService(db_connection)
        self.klass = klass

    @property
    def field_names(self) -> Tuple[str]:
        return data_class_fields_names(self.klass)

    def get_all(self) -> List[db.Acceptor]:
        return self.qs.fetch_all(self.klass)

    def get_details(self, id_):
        """Provides basic data for object by id. If any extra business logic needed,
        reimplement in the inherited class"""
        obj = self.qs.fetch_one(id_, self.klass)
        return obj

    def save(self):
        raise NotImplemented
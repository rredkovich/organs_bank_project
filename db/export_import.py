import sqlite3
from db import models, utilities, query_service
from settings import db_connection

class DBExporterImporter:
    def __init__(self):
        self.primary_models = (models.Donor, models.Acceptor,)
        self.fk_depenent_models =  (models.DonatedOrgan, models.AwaitedOrgan,)
        self.photo_models = (models.DonorPhoto, models.AcceptorPhoto,)
        self.handled_models = self.primary_models + self.fk_depenent_models + self.photo_models
        self.qs = query_service.QueryService(db_connection)

    def export_all(self, files_path: str):
        models = self.primary_models + self.fk_depenent_models
        fields = [utilities.data_class_fields_names(model) for model in models]
        tables = [utilities.class_to_table_name(model.__name__) for model in models]

        for i, model in enumerate(self.primary_models + self.fk_depenent_models):
            records = self.qs.fetch_all(model)
            values = [tuple(getattr(record, field).__str__() for field in fields[i]) for record in records]
            stmt = f"INSERT INTO {tables[i]} {tuple(fields[i])} VALUES {','.join(str(value) for value in values)};\n"

            stmts = [stmt, ]

            if model in self.primary_models:
                seq_stmt = f"UPDATE sqlite_sequence SET seq = {values[-1][0]} WHERE name = '{tables[i]}';\n"
                stmts.append(seq_stmt)

            with open(f"{files_path}/{tables[i]}.sql", "w") as f:
                f.writelines(stmts)

        for i, model in enumerate(self.photo_models):
            fields = [utilities.data_class_fields_names(model) for model in self.photo_models]
            tables = [utilities.class_to_table_name(model.__name__) for model in self.photo_models]
            records = self.qs.fetch_all(model)
            values = []
            for record in records:
                id_colname = fields[i][0]
                id_val = getattr(record, id_colname)
                photo_hex = f"X'{record.photo.hex()}'"
                values.append(f"({id_val}, {photo_hex})")
            stmt = f"INSERT INTO {tables[i]} {tuple(fields[i])} VALUES {','.join(values)};\n"

            with open(f"{files_path}/{tables[i]}.sql", "w", encoding='utf-8') as f:
                f.write(stmt)

    def import_all(self, files_path: str):
        for i, model in enumerate(self.handled_models):
            table_name = utilities.class_to_table_name(model.__name__)
            with open(f"{files_path}/{table_name}.sql", 'r') as f:
                data = f.readlines()
            if data:
                delete_stmt = f"DELETE FROM {table_name}"
                self.qs.execute(delete_stmt)
            for stmt in data:
                self.qs.execute(stmt)



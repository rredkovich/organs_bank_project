import sqlite3

from db.fixtures import gender_male, organ_heart
from db.query_service import QueryService
from db.models import Gender, Organ
from .fixtures import db_connection, gender_male, organ_heart, organ_kidney_a_negative

def test_prepare_dataclass(db_connection, gender_male):
    qs = QueryService(db_connection)
    t_name, cols, vals = qs._prepare_dataclass(gender_male)

    assert t_name == "genders"
    assert cols == ("gender",)
    assert vals == ("male",)


def test_prepare_dataclass_many_fields(db_connection, organ_heart):
    qs = QueryService(db_connection)
    t_name, cols, vals = qs._prepare_dataclass(organ_heart)
    assert t_name == "organs"
    assert cols == ("id", "organ_name", "blood_type",)
    assert vals == (organ_heart.id, organ_heart.organ_name, organ_heart.blood_type,)


def test_prepare_insert_stmt(db_connection, gender_male):
    qs = QueryService(db_connection)
    sql, values = qs._prepare_insert_stmt(gender_male)

    assert sql == "INSERT INTO genders (gender) VALUES (?) RETURNING *"
    assert values == ("male",)

def test_prepare_insert_stmt_many_fields(db_connection, organ_heart):
    qs = QueryService(db_connection)
    sql, values = qs._prepare_insert_stmt(organ_heart)
    assert sql == "INSERT INTO organs (organ_name, blood_type) VALUES (?, ?) RETURNING *"
    assert values == ("heart", "A+",)

def test_prepare_update_stmt_one_field(gender_male, db_connection):
    qs = QueryService(db_connection)

    sql, values = qs._prepare_update_stmt(gender_male)
    assert sql == "UPDATE genders SET gender = ? WHERE gender = ? RETURNING *"
    assert values == ("male",)

def test_prepare_update_stmt_many_fields_lib_table(organ_heart, db_connection):
    qs = QueryService(db_connection)

    sql, values = qs._prepare_update_stmt(organ_heart)
    assert sql == "UPDATE organs SET organ_name = ?, blood_type = ? WHERE id = ? RETURNING *"

def test_prepare_delete_stmt(organ_heart, db_connection):
    qs = QueryService(db_connection)
    sql, values = qs._prepare_delete_stmt(organ_heart)
    assert sql == "DELETE FROM organs WHERE id = ?"
    assert values == (organ_heart.id,)

def test_create(organ_kidney_a_negative, db_connection):
    qs = QueryService(db_connection)

    created_organ = qs.create(organ_kidney_a_negative)

    assert created_organ.id is not None

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM organs ORDER BY id DESC LIMIT 1")
    columns = (val[0] for val in cur.description)
    result = dict(zip(columns, cur.fetchone()))
    assert result["id"] == 1
    assert created_organ.id == result["id"]
    assert result["organ_name"] == organ_kidney_a_negative.organ_name
    assert result["blood_type"] == organ_kidney_a_negative.blood_type
    db_connection.commit()
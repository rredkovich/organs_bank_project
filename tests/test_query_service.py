from tests.fixtures import gender_male, organ_heart
from db.query_service import QueryService
from db.models import AwaitedOrgan
from tests.fixtures import db_connection, organ_kidney_a_negative, \
    organ_kidney_b_positive, acceptor

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
    assert cols == ("organ_id", "organ_name", "blood_type",)
    assert vals == (organ_heart.organ_id, organ_heart.organ_name, organ_heart.blood_type,)


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
    assert sql == "UPDATE genders SET gender = ? WHERE gender = ? RETURNING gender"
    assert values == ("male",)

def test_prepare_update_stmt_many_fields_lib_table(organ_heart, db_connection):
    qs = QueryService(db_connection)

    sql, values = qs._prepare_update_stmt(organ_heart)
    assert sql == ("UPDATE organs SET organ_name = ?, blood_type = ? WHERE organ_id = ? "
                   "RETURNING organ_id, organ_name, blood_type")
    assert values == ("heart", "A+", 1)

def test_prepare_delete_stmt(organ_heart, db_connection):
    qs = QueryService(db_connection)
    sql, values = qs._prepare_delete_stmt(organ_heart)
    assert sql == "DELETE FROM organs WHERE organ_id = ?"
    assert values == (organ_heart.organ_id,)

def test_create(organ_kidney_a_negative, db_connection):
    qs = QueryService(db_connection)

    created_organ = qs.create(organ_kidney_a_negative)

    assert created_organ.organ_id is not None

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM organs ORDER BY organ_id DESC LIMIT 1")
    columns = (val[0] for val in cur.description)
    result = dict(zip(columns, cur.fetchone()))
    assert result["organ_id"] == created_organ.organ_id
    assert result["organ_name"] == organ_kidney_a_negative.organ_name
    assert result["blood_type"] == organ_kidney_a_negative.blood_type
    db_connection.commit()

def test_create_with_fk(acceptor, organ_kidney_a_negative, db_connection):
    qs = QueryService(db_connection)

    kidney = qs.create(organ_kidney_a_negative)
    acceptor = qs.create(acceptor)

    awaited_organ = AwaitedOrgan(acceptor.acceptor_id, kidney.organ_name)

    awaited_organ = qs.create(awaited_organ)
    assert awaited_organ.acceptor_id == acceptor.acceptor_id

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM awaited_organs ORDER BY created_at DESC LIMIT 1")
    columns = (val[0] for val in cur.description)
    result = dict(zip(columns, cur.fetchone()))

    assert result["acceptor_id"] == acceptor.acceptor_id
    assert result["organ_name"] == organ_kidney_a_negative.organ_name
    db_connection.commit()

def test_update(organ_kidney_a_negative, db_connection):
    qs = QueryService(db_connection)

    created_organ = qs.create(organ_kidney_a_negative)

    assert created_organ.organ_id is not None

    created_organ.blood_type = 'B+'

    qs.update(created_organ)

    # assert awaited_organ.id is not None

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM organs where organ_id = ?", (created_organ.organ_id,))
    columns = (val[0] for val in cur.description)
    result = dict(zip(columns, cur.fetchone()))

    assert result["organ_name"] == organ_kidney_a_negative.organ_name
    assert result["blood_type"] == "B+"
    db_connection.commit()

def test_delete(organ_kidney_a_negative, db_connection):
    # TODO: allow deletion only from general tables, not library ones
    pass

def test_fetch_one(organ_kidney_a_negative, db_connection):
    qc = QueryService(db_connection)

    created = qc.create(organ_kidney_a_negative)
    assert created.organ_id is not None

    fetched = qc.fetch_one(created.organ_id, organ_kidney_a_negative.__class__)
    assert fetched.organ_id == created.organ_id
    assert fetched.organ_name == organ_kidney_a_negative.organ_name
    assert fetched.blood_type == organ_kidney_a_negative.blood_type

def test_fetch_filtered(organ_kidney_a_negative, organ_kidney_b_positive, db_connection):
    cur = db_connection.cursor()

    # erasing previous test data
    cur.execute("DELETE FROM organs")
    db_connection.commit()

    qs = QueryService(db_connection)
    one = qs.create(organ_kidney_a_negative)
    two = qs.create(organ_kidney_b_positive)

    kidneys = qs.fetch_filtered('organ_name', 'kidney', one.__class__)

    assert kidneys == [one, two]
from datetime import datetime
from db.query_service import QueryService, OrganMatchQueryService
from db.models import AwaitedOrgan
from .fixtures import *


def test_prepare_dataclass(db_connection, gender_male):
    qs = QueryService(db_connection)
    t_name, cols, vals = qs._prepare_dataclass(gender_male)

    assert t_name == "genders"
    assert cols == ("gender",)
    assert vals == ("male",)


def test_prepare_dataclass_many_fields(db_connection, acceptor_photo):
    qs = QueryService(db_connection)
    t_name, cols, vals = qs._prepare_dataclass(acceptor_photo)
    assert t_name == "acceptor_photos"
    assert cols == ("acceptor_id", "photo",)
    assert vals == (acceptor_photo.acceptor_id, acceptor_photo.photo,)


def test_prepare_insert_stmt(db_connection, gender_male):
    qs = QueryService(db_connection)
    sql, values = qs._prepare_insert_stmt(gender_male)

    assert sql == "INSERT INTO genders (gender) VALUES (?) RETURNING *"
    assert values == ("male",)


def test_prepare_insert_stmt_many_fields(db_connection, acceptor_a_pos):
    qs = QueryService(db_connection)
    sql, values = qs._prepare_insert_stmt(acceptor_a_pos)
    assert sql == 'INSERT INTO acceptors (name, registration_date, birthdate, blood_type, gender, height, weight, phone, address, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *'
    assert values == ('Alice Novak', datetime(2024, 5, 12).date(), datetime(1990, 8, 25).date(), 'A+', 'female', 165, 58, '555-1234', '123 Maple Street, Springfield', 'Diabetic')


def test_prepare_update_stmt_one_field(gender_male, db_connection):
    qs = QueryService(db_connection)

    sql, values = qs._prepare_update_stmt(gender_male)
    assert sql == "UPDATE genders SET gender = ? WHERE gender = ? RETURNING gender"
    assert values == ("male",)


def test_prepare_update_stmt_many_fields_lib_table(acceptor_a_pos, db_connection):
    qs = QueryService(db_connection)

    sql, values = qs._prepare_update_stmt(acceptor_a_pos)
    assert sql == ("UPDATE acceptors SET name = ?, registration_date = ?, birthdate = ?, blood_type = ?, gender = ?, "
        "height = ?, weight = ?, phone = ?, address = ?, notes = ? WHERE acceptor_id = ? RETURNING acceptor_id, name, "
        "registration_date, birthdate, blood_type, gender, height, weight, phone, address, notes")
    assert values == ('Alice Novak', datetime(2024, 5, 12).date(), datetime(1990, 8, 25).date(), 'A+', 'female', 165, 58, '555-1234', '123 Maple Street, Springfield', 'Diabetic', 1)


def test_prepare_delete_stmt(acceptor_a_pos, db_connection):
    qs = QueryService(db_connection)
    sql, values = qs._prepare_delete_stmt(acceptor_a_pos)
    assert sql == "DELETE FROM acceptors WHERE acceptor_id = ?"
    assert values == (acceptor_a_pos.acceptor_id,)


def test_create(acceptor_a_pos, db_connection):
    qs = QueryService(db_connection)

    created_organ = qs.create(acceptor_a_pos)

    assert created_organ.acceptor_id is not None

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM acceptors ORDER BY acceptor_id DESC LIMIT 1")
    columns = (val[0] for val in cur.description)
    result = dict(zip(columns, cur.fetchone()))
    assert result["acceptor_id"] == created_organ.acceptor_id
    assert result["name"] == acceptor_a_pos.name
    assert result["blood_type"] == acceptor_a_pos.blood_type
    db_connection.commit()


def test_create_with_fk(acceptor, organ_heart, db_connection):
    qs = QueryService(db_connection)

    acceptor = qs.create(acceptor)

    awaited_organ = AwaitedOrgan(acceptor.acceptor_id, organ_heart.organ_name)

    awaited_organ = qs.create(awaited_organ)
    assert awaited_organ.acceptor_id == acceptor.acceptor_id

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM awaited_organs ORDER BY created_at DESC LIMIT 1")
    columns = (val[0] for val in cur.description)
    result = dict(zip(columns, cur.fetchone()))

    assert result["acceptor_id"] == acceptor.acceptor_id
    assert result["organ_name"] == organ_heart.organ_name
    db_connection.commit()


def test_update(acceptor_a_pos, db_connection):
    qs = QueryService(db_connection)

    created = qs.create(acceptor_a_pos)

    assert created.acceptor_id is not None

    created.blood_type = 'B-'

    updated = qs.update(created)
    assert updated is not None

    # assert awaited_organ.id is not None

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM acceptors where acceptor_id = ?", (created.acceptor_id,))
    columns = (val[0] for val in cur.description)
    result = dict(zip(columns, cur.fetchone()))

    assert result["name"] == acceptor_a_pos.name
    assert result["blood_type"] == "B-"
    db_connection.commit()

def test_update_or_create(db_connection, acceptor):
    qs = QueryService(db_connection)
    qs.execute("DELETE FROM acceptors")
    precreated_id = acceptor.acceptor_id
    created = qs.update_or_create(acceptor)
    assert created is not None
    assert precreated_id != acceptor.acceptor_id


def test_delete(acceptor, db_connection):
    # TODO: allow deletion only from general tables, not library ones
    qs = QueryService(db_connection)
    created = qs.create(acceptor)

    qs.delete_fitered(created.__class__, 'acceptor_id', created.acceptor_id)

    result  = qs.execute("SELECT COUNT(*) FROM acceptors WHERE acceptor_id = ?", values=(created.acceptor_id, ))
    assert result[0] == (0,)



def test_fetch_one(acceptor_a_pos, db_connection):
    qc = QueryService(db_connection)

    created = qc.create(acceptor_a_pos)
    assert created.acceptor_id is not None
    acceptor_a_pos.acceptor_id = created.acceptor_id

    fetched = qc.fetch_one(created.acceptor_id, acceptor_a_pos.__class__)
    assert acceptor_a_pos == fetched


def test_fetch_filtered(acceptor_a_pos, acceptor3, db_connection):
    qs = QueryService(db_connection)
    qs.execute("DELETE FROM acceptors")
    one = qs.create(acceptor_a_pos)
    two = qs.create(acceptor3)

    accs = qs.fetch_filtered('gender', one.gender, one.__class__)

    assert accs == [one, two]


def test_add_photo(acceptor, acceptor_photo, db_connection):
    """Testing to be sure that bytes are stored as intended"""
    qs = QueryService(db_connection)

    acceptor = qs.create(acceptor)
    acceptor_photo.acceptor_id = acceptor.acceptor_id

    saved_photo = qs.create(acceptor_photo)

    stmt = "select * from acceptor_photos where acceptor_id = ?"
    cur = db_connection.cursor()
    cur.execute(stmt, (acceptor.acceptor_id,))
    data = cur.fetchone()

    assert data[1] == acceptor_photo.photo


def test_fetch_all(db_connection, acceptor_a_pos, acceptor2, acceptor3):
    cur = db_connection.cursor()

    # erasing previous test data
    data = cur.execute("DELETE FROM acceptors")
    db_connection.commit()

    qs = QueryService(db_connection)

    one = qs.create(acceptor_a_pos)
    three = qs.create(acceptor3)
    two = qs.create(acceptor2)

    all_accs = qs.fetch_all(one.__class__)

    assert all_accs == [one, three, two]


def test_format_dates(db_connection, acceptor):
    acceptor.registration_date = '2029-01-01'
    acceptor.birthdate = '1970-01-02'

    qs = QueryService(db_connection)

    qs._format_dates(acceptor)

    assert acceptor.registration_date == date(2029, 1, 1)
    assert acceptor.birthdate == date(1970, 1, 2)

def test_fetch_matched_donated_organs(db_connection,
                                      donor_a_positive,
                                      donor_a_negative,
                                      donated_blood,
                                      donated_blood2,
                                      acceptor_a_pos,
                                      blood
                                      ):
    qs = QueryService(db_connection)
    qs.execute("DELETE FROM acceptors")
    qs.execute("DELETE FROM donors")

    d_pos = qs.create(donor_a_positive)
    d_neg = qs.create(donor_a_negative)

    donated_blood.donor_id = d_pos.donor_id
    pos_donated_blood = qs.create(donated_blood)

    donated_blood2.donor_id = d_neg.donor_id
    neg_donated_blood = qs.create(donated_blood2)

    acceptor = qs.create(acceptor_a_pos)

    qqs = OrganMatchQueryService(db_connection)
    blood_matches = qqs.fetch_matched_donated_organs(acceptor.acceptor_id)

    # nothing asked from this acceptor
    assert len(blood_matches) == 0

    # adding requests for some blood
    requested_blood = AwaitedOrgan(
        acceptor_id=acceptor.acceptor_id,
        organ_name=blood.organ_name
    )
    qs.create(requested_blood)

    blood_matches = qqs.fetch_matched_donated_organs(acceptor.acceptor_id)
    assert len(blood_matches) == 1
    match = blood_matches[0]
    assert match.blood_type == acceptor.blood_type
    assert match.organ_name == pos_donated_blood.organ_name
    assert match.donor_id == donor_a_positive.donor_id
    assert match.donor_name == donor_a_positive.name

    print(match)
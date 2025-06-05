import sqlite3
from datetime import datetime, date

import pytest
from db.initialise_db import init_db
from db.models import BloodType, Organ, Gender, Acceptor


@pytest.fixture(scope="session")
def db_connection():
    conn = sqlite3.connect(":memory:")
    # setup schema
    init_db(conn)
    yield conn
    conn.close()

@pytest.fixture
def gender_male():
    return Gender("male")

@pytest.fixture
def gender_female():
    return Gender("female")

@pytest.fixture
def blood_type_a_positive():
    return BloodType("A+")

@pytest.fixture
def blood_type_a_negative():
    return BloodType("A-")

@pytest.fixture
def organ_heart():
    return Organ(
        organ_id=1,
        organ_name="heart",
        blood_type="A+",
    )

# TODO: fixture reuse don't work here!
@pytest.fixture
def organ_kidney_a_negative():
    return Organ(
        organ_id=2,
        organ_name="kidney",
        blood_type="A-"
    )

@pytest.fixture
def organ_kidney_b_positive():
    return Organ(
        organ_id=2,
        organ_name="kidney",
        blood_type="B+"
    )

# # TODO: fixture reuse don't work here!
# @pytest.fixture
# def organ_kidney_a_negative(blood_type_a_negative):
#     return Organ(
#         id=2,
#         organ_name="kidney",
#         blood_type=blood_type_a_negative.blood_type
#     )

@pytest.fixture
def acceptor():
    return Acceptor(
        acceptor_id=None,
        name='Lina Doe',
        registration_date=datetime.now().date(),
        birthdate=date(1970, 1, 12),
        blood_type="A-",
        gender="female",
        height=176,
        weight=59,
        phone='0000000',
        address='fake one',
        notes=''
    )
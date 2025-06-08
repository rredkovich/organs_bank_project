import pytest
import sqlite3
from datetime import datetime, date

from db.initialise_db import init_db
from db.models import BloodType, Gender, Acceptor, Donor, AcceptorPhoto, DonatedOrgan, OrganName


@pytest.fixture
def photo():
    return "Photo"

@pytest.fixture(scope="session")
def db_connection():
    conn = sqlite3.connect(":memory:")
    # conn = sqlite3.connect("test.db")
    conn.execute("PRAGMA foreign_keys = ON")
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
def organ_heart(blood_type_a_positive):
    return OrganName(
        organ_name="heart",
    )
#
# @pytest.fixture
# def organ_kidney_a_negative(blood_type_a_negative):
#     return Organ(
#         organ_id=2,
#         organ_name="kidney",
#         blood_type=blood_type_a_negative.blood_type
#     )
#
# @pytest.fixture
# def organ_kidney_b_positive():
#     return Organ(
#         organ_id=2,
#         organ_name="kidney",
#         blood_type="B+"
#     )
#
# @pytest.fixture
# def blood_a_positive(blood_type_a_positive):
#     return Organ(
#         organ_id=0,
#         organ_name="blood",
#         blood_type=blood_type_a_positive.blood_type
#     )
#
# @pytest.fixture
# def blood_a_negative(blood_type_a_negative):
#     return Organ(
#         organ_id=0,
#         organ_name="blood",
#         blood_type=blood_type_a_negative.blood_type
#     )

@pytest.fixture
def acceptor(gender_female, blood_type_a_negative):
    return Acceptor(
        acceptor_id=None,
        name='Lina Doe',
        registration_date=datetime.now().date(),
        birthdate=date(1970, 1, 12),
        blood_type=blood_type_a_negative.blood_type,
        gender=gender_female.gender,
        height=176,
        weight=59,
        phone='0000000',
        address='fake one',
        notes=''
    )

@pytest.fixture
def acceptor_a_pos():
    return Acceptor(
        acceptor_id=1,
        name="Alice Novak",
        registration_date=date(2024, 5, 12),
        birthdate=date(1990, 8, 25),
        blood_type="A+",
        gender="female",
        height=165,
        weight=58,
        phone="555-1234",
        address="123 Maple Street, Springfield",
        notes="Diabetic"
    )

@pytest.fixture
def acceptor2():
    return Acceptor(
        acceptor_id=2,
        name="Bob Larsen",
        registration_date=date(2024, 6, 1),
        birthdate=date(1982, 3, 10),
        blood_type="O-",
        gender="male",
        height=178,
        weight=82,
        phone="555-5678",
        address="45 Oak Avenue, Lakeview",
        notes=None
    )

@pytest.fixture
def acceptor3():
    return Acceptor(
        acceptor_id=3,
        name="Carla Gomez",
        registration_date=date(2025, 1, 15),
        birthdate=date(1975, 11, 5),
        blood_type="B+",
        gender="female",
        height=160,
        weight=70,
        phone="771-2285",
        address="987 Pine Road, Hilltown",
        notes="Requires dialysis"
    )

@pytest.fixture
def acceptor4():
    return Acceptor(
        acceptor_id=4,
        name="Daniel Zhang",
        registration_date=date(2025, 3, 2),
        birthdate=date(2001, 4, 17),
        blood_type=None,
        gender="male",
        height=167,
        weight=58,
        phone="555-9012",
        address='',
        notes="Recently added, awaiting full medical evaluation"
    )

@pytest.fixture
def donor_a_positive(blood_type_a_positive, gender_male):
    return Donor(
        donor_id=0,
        name='John Doe A+',
        registration_date=datetime.now().date(),
        birthdate= datetime(1999, 1, 1),
        blood_type= blood_type_a_positive.blood_type,
        possible_extraction= datetime.now().date(),
        gender= gender_male.gender
    )

@pytest.fixture
def donor_a_negative(blood_type_a_negative, gender_male):
    return Donor(
        donor_id=0,
        name='John Smith A-',
        registration_date=datetime.now().date(),
        birthdate=datetime(1999, 1, 1),
        blood_type= blood_type_a_negative.blood_type,
        possible_extraction= datetime.now().date(),
        gender= gender_male.gender
    )

@pytest.fixture
def blood():
    return OrganName(organ_name='blood')

@pytest.fixture
def donated_blood():
    return DonatedOrgan(
    donor_id=0,
    organ_name="blood",
    extraction_ts=datetime.now().date(),
    )

@pytest.fixture
def donated_blood2():
    return DonatedOrgan(
        donor_id=0,
        organ_name="blood",
        extraction_ts=datetime.now().date(),
    )


@pytest.fixture
def man_photo():
    # path = Path("tests")
    with open("tests/man-face.png", "rb") as f:
        photo = f.read()
    return photo

@pytest.fixture
def acceptor_photo(man_photo):
    return AcceptorPhoto(
        acceptor_id=None,
        photo=man_photo,
    )
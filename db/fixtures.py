import pytest
from db.models import BloodType, Organ, Gender

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
        organ_name="heart",
        blood_type="A+",
    )

# TODO: fixture reuse don't work here!
@pytest.fixture
def kidney_a_negative(blood_type_a_negative):
    return Organ(
        organ_name="kidney",
        blood_type=blood_type_a_negative.blood_type
    )
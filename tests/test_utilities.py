import pytest
from tests.fixtures import acceptor
from db.utilities import camel_to_snake, pluralize, class_to_table_name, primary_key_by_class
from db.models import BloodType, Gender


def test_camel_to_snake():
    camel = "BloodType"
    assert camel_to_snake(camel) == "blood_type"


def test_pluralize():
    assert pluralize("BloodType") == "BloodTypes"
    assert pluralize("City") == "Cities"


def test_class_to_table_name():
    blood_type = BloodType("A+")
    gender = Gender("female")
    assert class_to_table_name(blood_type.__class__.__name__) == "blood_types"
    assert class_to_table_name(gender.__class__.__name__) == "genders"


def test_gather_primary_key_by_class(acceptor):

    assert primary_key_by_class(acceptor.__class__) == "acceptor_id"
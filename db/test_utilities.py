import pytest
from .utilities import camel_to_snake, pluralize, class_to_table_name
from .models import BloodType, Gender

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


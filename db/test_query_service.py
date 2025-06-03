import sqlite3

from db.fixtures import gender_male, organ_heart
from db.query_service import QueryService
from db.models import Gender, Organ
from .fixtures import gender_male, organ_heart

conn = sqlite3.connect('test.db')

def test_prepare_dataclass(gender_male):
    qs = QueryService(conn)
    t_name, cols, vals = qs._prepare_dataclass(gender_male)

    assert t_name == "genders"
    assert cols == ("gender",)
    assert vals == ("male",)


def test_prepare_dataclass_many_fields(organ_heart):
    qs = QueryService(conn)
    t_name, cols, vals = qs._prepare_dataclass(organ_heart)
    assert t_name == "organs"
    assert cols == ("organ_name", "blood_type",)
    assert vals == ("heart", "A+",)

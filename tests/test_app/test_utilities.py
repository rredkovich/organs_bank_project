from app.views.utilities import calc_column_width

def test__calc_column_width():
    assert calc_column_width('four', 0, multiplier=10) == 42
    assert calc_column_width('1', 'five_', multiplier=10) == 52

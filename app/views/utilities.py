def calc_column_width(col_name, col_value, multiplier=10):
    """Calculates column width for a table view"""
    widest = max((col_name, col_value,), key=lambda x: len(str(x)))
    return round(len(str(widest)) * multiplier + len(str(widest)) * 0.45)
from datetime import datetime


def get_date(date):
    try:
        year, month, day = date.split('-')
        return datetime(int(year), int(month), int(day))
    except Exception:
        raise ValueError("Date format is not correct, it should be yyyy-mm-dd")

from datetime import datetime
from flask_restful import abort


def get_date(date):
    try:
        day, month, year = date.split('-')
        return datetime(int(year), int(month), int(day))
    except Exception:
        abort(400, message='Wrong parameters')


def get_boolean(argument):
    if argument == 'True':
        argument = True
    elif argument == 'False':
        argument = False
    else:
        abort(400, message='Wrong parameters')

    return argument


def get_int(argument):
    try:
        return int(argument)
    except Exception:
        return None


def get_float(argument):
    try:
        return float(argument)
    except Exception:
        return None


def get_checkbox(argument):
    if argument == 'on':
        return True
    else:
        return False

from functools import wraps
from flask import request
from flask_restful import abort

from menu_planning.services.user_service import UserService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.cookies.get('username')
        password = request.cookies.get('password')

        user = UserService.get_user(username, password)
        if user is None:
            abort(401, error='Unauthorized')
        return f(*args, **kwargs)
    return decorated_function

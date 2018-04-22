from menu_planning.models import User


class UserService:

    @staticmethod
    def get_user(username, password):
        return User.query.filter_by(username=username, password=password).first()
from menu_planning.models import Starter
from sqlalchemy.sql.expression import func


class StarterService:

    def get_by_id(self, id):
        return Starter.query.filter_by(id=id).first()

    def get_random(self):
        return Starter.query.order_by(func.rand()).first()

    def get_all(self):
        return Starter.query.all()

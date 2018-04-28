from menu_planning.models import Food, db, DailyMenu
from sqlalchemy import or_


class FoodService:

    def create(self, name, type, url=None):
        food = Food(name, type, url)
        db.session.add(food)
        db.session.commit()
        return food

    def get_by_id(self, id):
        return Food.query.filter_by(id=id).first()

    def get_all(self):
        return Food.query.all()

    def get_by_menu_id(self, menu_id):
        return Food.query.\
            join(DailyMenu, or_(DailyMenu.lunch_id == Food.id,
                                DailyMenu.starter_id == Food.id,
                                DailyMenu.dinner_id == Food.id)).\
            filter(DailyMenu.menu_id == menu_id).all()

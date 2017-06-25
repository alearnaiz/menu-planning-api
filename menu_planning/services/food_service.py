from menu_planning.models import Food, db


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

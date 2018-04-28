from menu_planning.models import FoodIngredient
from menu_planning import db


class FoodIngredientService:

    def get_all_by_food_id(self, food_id):
        return FoodIngredient.query.filter_by(food_id=food_id).all()

    def delete_all_by_food_id(self, food_id):
        FoodIngredient.query.filter_by(food_id=food_id).delete()
        db.session.commit()

    def create(self, food_id, ingredient_id, quantity=None):
        food_ingredient = FoodIngredient(food_id=food_id, ingredient_id=ingredient_id, quantity=quantity)
        db.session.add(food_ingredient)
        db.session.commit()
        return food_ingredient


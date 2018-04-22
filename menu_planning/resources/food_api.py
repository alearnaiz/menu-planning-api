from menu_planning import api
from flask_restful import Resource, marshal_with, abort

from menu_planning.resources.login_decorator import login_required
from menu_planning.resources.output_fields import foods_fields, food_with_ingredients_fields
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.food_service import FoodService
from menu_planning.services.ingredient_service import IngredientService


class FoodListApi(Resource):

    @login_required
    @marshal_with(foods_fields)
    def get(self):
        food_service = FoodService()
        return food_service.get_all()

api.add_resource(FoodListApi, '/foods')


class FoodApi(Resource):

    @login_required
    @marshal_with(food_with_ingredients_fields)
    def get(self, food_id):
        food = check_food(food_id)

        ingredient_service = IngredientService()
        food_ingredient_service = FoodIngredientService()

        food_ingredients = food_ingredient_service.get_all_by_food_id(food.id)
        food.ingredients = []
        for food_ingredient in food_ingredients:
            food_ingredient.name = ingredient_service.get_by_id(food_ingredient.ingredient_id).name
            food.ingredients.append(food_ingredient)
        return food

api.add_resource(FoodApi, '/foods/<int:food_id>')


def check_food(food_id, food_service=FoodService()):
    food = food_service.get_by_id(id=food_id)
    if not food:
        abort(404, error='Food {} does not exist'.format(food_id))

    return food


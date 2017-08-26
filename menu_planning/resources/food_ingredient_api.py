from flask import request

from menu_planning import api
from flask_restful import Resource, abort

from menu_planning.models.schemas import parser_request, food_ingredient_schema
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.food_service import FoodService


class FoodIngredientListApi(Resource):

    def put(self, food_id):
        check_food(food_id)

        # Request
        parser = parser_request(request, food_ingredient_schema)

        food_ingredient_service = FoodIngredientService()
        food_ingredient_service.delete_all_by_food_id(food_id)
        for food_ingredient in parser:
            quantity = food_ingredient.get('quantity')
            food_ingredient_service.create(food_id=food_id, ingredient_id=food_ingredient.get('ingredient').get('id'),
                                           quantity=quantity)

        return 'Ingredients for the food {} updated'.format(food_id)

api.add_resource(FoodIngredientListApi, '/foods/<int:food_id>/ingredients')


def check_food(food_id, food_service=FoodService()):
    food = food_service.get_by_id(id=food_id)
    if not food:
        abort(404, error='Food {} does not exist'.format(food_id))

    return food

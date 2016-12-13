from flask import request
from menu_planning import api
from flask_restful import Resource, marshal_with, abort
from menu_planning.apis.resources import foods_fields, food_with_ingredients_fields
from menu_planning.apis.utils import get_int, get_boolean
from menu_planning.models import FoodType
from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.food_service import FoodService
from menu_planning.services.ingredient_service import IngredientService
from menu_planning.services.lunch_service import LunchService
from menu_planning.services.starter_service import StarterService


class FoodListApi(Resource):

    @marshal_with(foods_fields)
    def get(self):
        food_service = FoodService()

        return food_service.get_all()

    @marshal_with(foods_fields)
    def post(self):
        name = request.form.get('name')
        type = get_int(request.form.get('type'))

        if not name or type not in list(map(int, FoodType)):
            abort(400, message='Wrong parameters')

        if type == FoodType.starter.value:
            food_service = FoodService()
            starter_service = StarterService()

            food = food_service.create(name, type)
            starter_service.create(food.id)
        elif type == FoodType.lunch.value:
            need_starter = get_boolean(request.form.get('need_starter'))
            days = get_int(request.form.get('days'))
            related_dinner_id = get_int(request.form.get('related_dinner_id'))

            food_service = FoodService()
            lunch_service = LunchService()
            food = food_service.create(name, type)
            lunch_service.create(food.id, days=days, need_starter=need_starter, related_dinner_id=related_dinner_id)
        else:
            days = get_int(request.form.get('days'))

            food_service = FoodService()
            food = food_service.create(name, type)
            dinner_service = DinnerService()
            dinner_service.create(food.id, days)

        return food


api.add_resource(FoodListApi, '/foods')


class FoodApi(Resource):

    @marshal_with(food_with_ingredients_fields)
    def get(self, food_id):
        food_service = FoodService()

        food = food_service.get_by_id(id=food_id)
        if not food:
            abort(404, message="Food {} doesn't exist".format(food_id))

        ingredient_service = IngredientService()
        food_ingredient_service = FoodIngredientService()

        food_ingredients = food_ingredient_service.get_all_by_food_id(food.id)
        food.ingredients = []
        for food_ingredient in food_ingredients:
            food_ingredient.name = ingredient_service.get_by_id(food_ingredient.ingredient_id).name
            food.ingredients.append(food_ingredient)
        return food

api.add_resource(FoodApi, '/foods/<int:food_id>')

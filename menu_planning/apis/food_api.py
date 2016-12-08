from menu_planning import api
from flask_restful import Resource, marshal_with, abort
from menu_planning.apis.resources import foods_fields, food_with_ingredients_fields
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
        starter_service = StarterService()
        lunch_service = LunchService()
        dinner_service = DinnerService()

        starters = starter_service.get_all()
        lunches = lunch_service.get_all()
        dinners = dinner_service.get_all()

        foods = {
            'starters': starters,
            'lunches': lunches,
            'dinners': dinners,
        }

        return foods

api.add_resource(FoodListApi, '/foods')


class FoodApi(Resource):

    @marshal_with(food_with_ingredients_fields)
    def get(self, food_id):
        food_service = FoodService()

        food = food_service.get_by_id(id=food_id)
        if not food:
            abort(404, message="Food {} doesn't exist".format(food_id))

        starter_service = StarterService()
        lunch_service = LunchService()
        dinner_service = DinnerService()
        ingredient_service = IngredientService()
        food_ingredient_service = FoodIngredientService()

        if food.type == FoodType.starter.value:
            food = starter_service.get_by_id(food.id)
        elif food.type == FoodType.lunch.value:
            food = lunch_service.get_by_id(food.id)
        elif food.type == FoodType.dinner.value:
            food = dinner_service.get_by_id(food.id)

        food_ingredients = food_ingredient_service.get_all_by_food_id(food.id)
        food.ingredients = []
        for food_ingredient in food_ingredients:
            food_ingredient.name = ingredient_service.get_by_id(food_ingredient.ingredient_id).name
            food.ingredients.append(food_ingredient)
        return food

api.add_resource(FoodApi, '/foods/<int:food_id>')

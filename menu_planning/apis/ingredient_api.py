from flask import request
from menu_planning import api
from flask_restful import Resource, marshal_with, abort
from menu_planning.apis.resources import ingredient_fields
from menu_planning.apis.utils import get_float
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.ingredient_service import IngredientService


class IngredientListApi(Resource):

    @marshal_with(ingredient_fields)
    def get(self):
        ingredient_service = IngredientService()
        return ingredient_service.get_all()

    @marshal_with(ingredient_fields)
    def post(self):
        name = request.form.get('name')

        if not name:
            abort(400, message='Wrong parameters')

        ingredient_service = IngredientService()
        ingredient = ingredient_service.create(name=name)
        return ingredient, 201

api.add_resource(IngredientListApi, '/ingredients')


class FoodIngredientListApi(Resource):

    def put(self, food_id):
        food_ingredient_service = FoodIngredientService()
        food_ingredient_service.delete_all_by_food_id(food_id)

        ingredients = request.form.getlist('ingredients[]')

        for ingredient_id in ingredients:
            quantity = get_float(request.form.get('quantity_{}'.format(ingredient_id)))
            if quantity and quantity <= 0:
                quantity = None
            food_ingredient_service.create(food_id=food_id, ingredient_id=ingredient_id, quantity=quantity)

        return 'Ingredients for the food {} updated'.format(food_id)

api.add_resource(FoodIngredientListApi, '/foods/<int:food_id>/ingredients')

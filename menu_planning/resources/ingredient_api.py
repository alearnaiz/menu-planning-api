from menu_planning import api
from flask_restful import Resource, marshal_with, reqparse
from menu_planning.resources.output_fields import ingredient_fields
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.ingredient_service import IngredientService


class IngredientListApi(Resource):

    @marshal_with(ingredient_fields)
    def get(self):
        ingredient_service = IngredientService()
        return ingredient_service.get_all()

    @marshal_with(ingredient_fields)
    def post(self):
        # Body
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        name = args.get('name')

        ingredient_service = IngredientService()
        ingredient = ingredient_service.create(name=name)
        return ingredient, 201

api.add_resource(IngredientListApi, '/ingredients')


class FoodIngredientListApi(Resource):

    def put(self, food_id):
        food_ingredient_service = FoodIngredientService()
        food_ingredient_service.delete_all_by_food_id(food_id)

        # Body
        parser = reqparse.RequestParser()
        parser.add_argument('ingredient_id', action='append', type=int, required=True)
        args = parser.parse_args()
        ingredients = args.get('ingredient_id')
        parser = reqparse.RequestParser()
        for ingredient_id in ingredients:
            parser.add_argument('quantity_{}'.format(ingredient_id), type=float, required=False)
        args = parser.parse_args()

        for ingredient_id in ingredients:
            quantity = args.get('quantity_{}'.format(ingredient_id))
            if quantity and quantity <= 0:
                quantity = None
            food_ingredient_service.create(food_id=food_id, ingredient_id=ingredient_id, quantity=quantity)

        return 'Ingredients for the food {} updated'.format(food_id)

api.add_resource(FoodIngredientListApi, '/foods/<int:food_id>/ingredients')

from flask import request
from menu_planning import api
from flask_restful import Resource, marshal_with, abort
from menu_planning.apis.resources import ingredient_fields
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

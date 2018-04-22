from flask import request

from menu_planning import api
from flask_restful import Resource, marshal_with

from menu_planning.models.schemas import ingredient_schema, parser_request
from menu_planning.resources.login_decorator import login_required
from menu_planning.resources.output_fields import ingredient_fields
from menu_planning.services.ingredient_service import IngredientService


class IngredientListApi(Resource):

    @login_required
    @marshal_with(ingredient_fields)
    def get(self):
        ingredient_service = IngredientService()
        return ingredient_service.get_all()

    @login_required
    @marshal_with(ingredient_fields)
    def post(self):
        # Request
        parser = parser_request(request, ingredient_schema)
        name = parser.get('name')

        ingredient_service = IngredientService()
        ingredient = ingredient_service.create(name=name)
        return ingredient, 201

api.add_resource(IngredientListApi, '/ingredients')

from flask_restful import Resource, marshal_with, request

from menu_planning.models.schemas import starter_schema, parser_request
from menu_planning.resources.output_fields import starter_fields
from menu_planning import api
from menu_planning.models import FoodType
from menu_planning.services.food_service import FoodService
from menu_planning.services.starter_service import StarterService


class StarterListApi(Resource):

    @marshal_with(starter_fields)
    def get(self):
        starter_service = StarterService()
        return starter_service.get_all()

    @marshal_with(starter_fields)
    def post(self):
        # Request
        parser = parser_request(request, starter_schema)
        name = parser.get('name')
        url = parser.get('url')

        food_service = FoodService()
        starter_service = StarterService()

        food = food_service.create(name, FoodType.starter.value, url)
        starter = starter_service.create(food.id)

        return starter, 201

api.add_resource(StarterListApi, '/starters')

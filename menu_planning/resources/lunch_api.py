from flask import request
from flask_restful import Resource, marshal_with

from menu_planning.models.schemas import lunch_schema, parser_request
from menu_planning.resources.output_fields import lunch_fields
from menu_planning import api
from menu_planning.models import FoodType
from menu_planning.resources.validator import Validator
from menu_planning.services.food_service import FoodService
from menu_planning.services.lunch_service import LunchService


class LunchListApi(Resource):

    @marshal_with(lunch_fields)
    def get(self):
        lunch_service = LunchService()
        return lunch_service.get_all()

    @marshal_with(lunch_fields)
    def post(self):
        # Request
        parser = parser_request(request, lunch_schema)
        name = parser.get('name')
        url = parser.get('url')
        need_starter = parser.get('need_starter')
        days = parser.get('days')
        related_dinner_id = parser.get('related_dinner_id')

        food_service = FoodService()
        lunch_service = LunchService()
        food = food_service.create(name, FoodType.lunch.value, url)
        lunch = lunch_service.create(food.id, days=days, need_starter=need_starter, related_dinner_id=related_dinner_id)

        return lunch, 201


api.add_resource(LunchListApi, '/lunches')


class LunchApi(Resource):

    @marshal_with(lunch_fields)
    def get(self, lunch_id):
        return Validator.check_lunch(lunch_id)


api.add_resource(LunchApi, '/lunches/<int:lunch_id>')


from flask import request
from flask_restful import Resource, marshal_with, abort
from menu_planning import api
from menu_planning.models.schemas import parser_request, dinner_schema
from menu_planning.resources.output_fields import dinner_fields
from menu_planning.models import FoodType
from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.food_service import FoodService


class DinnerListApi(Resource):

    @marshal_with(dinner_fields)
    def get(self):
        dinner_service = DinnerService()
        return dinner_service.get_all()

    @marshal_with(dinner_fields)
    def post(self):
        # Request
        parser = parser_request(request, dinner_schema)
        name = parser.get('name')
        url = parser.get('url')
        days = parser.get('days')

        food_service = FoodService()
        food = food_service.create(name, FoodType.dinner.value, url)
        dinner_service = DinnerService()
        dinner = dinner_service.create(food.id, days)

        return dinner, 201

api.add_resource(DinnerListApi, '/dinners')


class DinnerApi(Resource):

    @marshal_with(dinner_fields)
    def get(self, dinner_id):
        return check_dinner(dinner_id)

api.add_resource(DinnerApi, '/dinners/<int:dinner_id>')


def check_dinner(dinner_id, dinner_service=DinnerService()):
    dinner = dinner_service.get_by_id(id=dinner_id)
    if not dinner:
        abort(404, error='Dinner {} does not exist'.format(dinner_id))

    return dinner

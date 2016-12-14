from flask_restful import Resource, abort, marshal_with
from flask import request
from menu_planning import api
from menu_planning.apis.resources import dinner_fields
from menu_planning.apis.utils import get_int
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
        name, days = check_request(request)

        food_service = FoodService()
        food = food_service.create(name, FoodType.dinner.value)
        dinner_service = DinnerService()
        dinner = dinner_service.create(food.id, days)

        return dinner, 201

api.add_resource(DinnerListApi, '/dinners')


def check_request(request):
    name = request.form.get('name')
    days = get_int(request.form.get('days'))

    if not name:
        abort(400, message='Wrong parameters')

    return name, days

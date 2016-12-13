from flask_restful import Resource, abort, marshal_with
from flask import request
from menu_planning import api
from menu_planning.apis.resources import lunch_fields
from menu_planning.apis.utils import get_int, get_boolean
from menu_planning.models import FoodType
from menu_planning.services.food_service import FoodService
from menu_planning.services.lunch_service import LunchService


class LunchListApi(Resource):

    @marshal_with(lunch_fields)
    def get(self):
        lunch_service = LunchService()
        return lunch_service.get_all()

    @marshal_with(lunch_fields)
    def post(self):
        name = request.form.get('name')

        if not name:
            abort(400, message='Wrong parameters')

        need_starter = get_boolean(request.form.get('need_starter'))
        days = get_int(request.form.get('days'))
        related_dinner_id = get_int(request.form.get('related_dinner_id'))

        food_service = FoodService()
        lunch_service = LunchService()
        food = food_service.create(name, FoodType.lunch.value)
        lunch = lunch_service.create(food.id, days=days, need_starter=need_starter, related_dinner_id=related_dinner_id)

        return lunch, 201

api.add_resource(LunchListApi, '/lunches')

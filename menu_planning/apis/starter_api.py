from flask_restful import Resource, abort, marshal_with
from flask import request
from menu_planning import api
from menu_planning.apis.resources import starter_fields
from menu_planning.apis.utils import get_int
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
        name = request.form.get('name')

        if not name:
            abort(400, message='Wrong parameters')

        food_service = FoodService()
        starter_service = StarterService()

        food = food_service.create(name, FoodType.starter.value)
        starter = starter_service.create(food.id)

        return starter, 201

api.add_resource(StarterListApi, '/starters')

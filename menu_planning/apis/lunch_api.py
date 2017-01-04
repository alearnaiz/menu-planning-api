from flask_restful import Resource, marshal_with, reqparse, inputs
from menu_planning.apis.resources import lunch_fields
from menu_planning import api
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
        # Body
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('need_starter', type=inputs.boolean, required=True)
        parser.add_argument('days', type=int, required=False)
        parser.add_argument('related_dinner_id', type=int, required=False)
        args = parser.parse_args()
        name = args.get('name')
        need_starter = args.get('need_starter')
        days = args.get('days')
        related_dinner_id = args.get('related_dinner_id')

        food_service = FoodService()
        lunch_service = LunchService()
        food = food_service.create(name, FoodType.lunch.value)
        lunch = lunch_service.create(food.id, days=days, need_starter=need_starter, related_dinner_id=related_dinner_id)

        return lunch, 201

api.add_resource(LunchListApi, '/lunches')

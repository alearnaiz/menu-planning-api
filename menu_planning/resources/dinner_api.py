from flask_restful import Resource, marshal_with, reqparse
from menu_planning import api
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
        # Body
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('url', type=str, required=False)
        parser.add_argument('days', type=int, required=False)
        args = parser.parse_args()
        name = args.get('name')
        url = args.get('url')
        days = args.get('days')

        food_service = FoodService()
        food = food_service.create(name, FoodType.dinner.value, url)
        dinner_service = DinnerService()
        dinner = dinner_service.create(food.id, days)

        return dinner, 201

api.add_resource(DinnerListApi, '/dinners')

from menu_planning import api
from flask_restful import Resource, marshal_with, abort, reqparse, inputs
from menu_planning.actions.menu_generator import MenuGenerator
from menu_planning.services.daily_menu_service import DailyMenuService
from menu_planning.services.menu_service import MenuService
from menu_planning.apis.resources import menu_fields, menu_with_daily_menus_fields
from menu_planning.apis import utils
from datetime import date


class MenuListApi(Resource):

    @marshal_with(menu_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all()

    @marshal_with(menu_fields)
    def post(self):
        # Body
        parser = reqparse.RequestParser()
        parser.add_argument('start_lunch', type=inputs.boolean, required=True)
        parser.add_argument('end_dinner', type=inputs.boolean, required=True)
        parser.add_argument('start_date', type=utils.get_date, required=True)
        parser.add_argument('end_date', type=utils.get_date, required=True)
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('favourite', type=inputs.boolean, required=False)
        args = parser.parse_args()
        start_lunch = args.get('start_lunch')
        end_dinner = args.get('end_dinner')
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        name = args.get('name')
        favourite = args.get('favourite')

        try:
            days = (end_date - start_date).days + 1

            menu_generator = MenuGenerator()
            menu = menu_generator.generate(days=days, start_date=start_date, start_lunch=start_lunch,
                                           end_dinner=end_dinner)

            if name and favourite:
                menu_service = MenuService()
                menu_service.update(menu.id, name=name, favourite=favourite)
            elif name:
                menu_service = MenuService()
                menu_service.update(menu.id, name=name)
            elif favourite:
                menu_service = MenuService()
                menu_service.update(menu.id, favourite=favourite)

        except Exception as exception:
            abort(400, error=str(exception))

        return menu, 201

api.add_resource(MenuListApi, '/menus')


class MenuApi(Resource):

    @marshal_with(menu_with_daily_menus_fields)
    def get(self, menu_id):
        return check_menu(menu_id)

    def put(self, menu_id):
        menu_service = MenuService()
        menu = check_menu(menu_id, menu_service)

        # Body
        parser = reqparse.RequestParser()
        for daily_menu in menu.daily_menus:
            parser.add_argument('starter_id[' + str(daily_menu.day) + ']', type=int, required=False)
            parser.add_argument('lunch_id[' + str(daily_menu.day) + ']', type=int, required=False)
            parser.add_argument('dinner_id[' + str(daily_menu.day) + ']', type=int, required=False)
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('favourite', type=inputs.boolean, required=True)
        args = parser.parse_args()
        name = args.get('name')
        favourite = args.get('favourite')

        # Update menu
        menu_service.update(menu_id, name=name, favourite=favourite)

        # Update daily menus
        daily_menu_service = DailyMenuService()
        for daily_menu in menu.daily_menus:
            starter_id = args.get('starter_id[' + str(daily_menu.day) + ']')
            lunch_id = args.get('lunch_id[' + str(daily_menu.day) + ']')
            dinner_id = args.get('dinner_id[' + str(daily_menu.day) + ']')

            daily_menu.starter_id = starter_id
            daily_menu.lunch_id = lunch_id
            daily_menu.dinner_id = dinner_id

            daily_menu_service.update(daily_menu)

        return 'Menu {} updated'.format(menu_id)

api.add_resource(MenuApi, '/menus/<int:menu_id>')


class FavouriteMenuListApi(Resource):

    @marshal_with(menu_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all_by_favourites()

api.add_resource(FavouriteMenuListApi, '/menus/favourites')


class CurrentMenuListApi(Resource):

    @marshal_with(menu_with_daily_menus_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all_by_date(date.today())

api.add_resource(CurrentMenuListApi, '/menus/current')


def check_menu(menu_id, menu_service=MenuService()):
    menu = menu_service.get_by_id(menu_id)

    if not menu:
        abort(404, error='Menu {} does not exist'.format(menu_id))

    return menu

from datetime import date

from flask_restful import Resource, marshal_with, abort, request

from menu_planning import api
from menu_planning.actions.menu_generator import MenuGenerator
from menu_planning.models.schemas import parser_request, menu_with_daily_menus_schema, create_menu_schema
from menu_planning.resources.output_fields import menu_fields, menu_with_daily_menus_fields
from menu_planning.services.daily_menu_service import DailyMenuService
from menu_planning.services.menu_service import MenuService


class MenuListApi(Resource):

    @marshal_with(menu_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all()

    @marshal_with(menu_fields)
    def post(self):
        # Request
        parser = parser_request(request, create_menu_schema)
        start_lunch = parser.get('start_lunch')
        end_dinner = parser.get('end_dinner')
        start_date = parser.get('start_date')
        end_date = parser.get('end_date')
        name = parser.get('name')
        favourite = parser.get('favourite')

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
        check_menu(menu_id, menu_service)

        # Request
        parser = parser_request(request, menu_with_daily_menus_schema)
        name = parser.get('name')
        favourite = parser.get('favourite')

        # Update daily menus
        daily_menu_service = DailyMenuService()
        for daily_menu_data in parser.get('daily_menus'):
            daily_menu = check_daily_menu(menu_id, daily_menu_data.get('id'))
            daily_menu.starter_id = daily_menu_data.get('starter').get('id') if daily_menu_data.get('starter') else None
            daily_menu.lunch_id = daily_menu_data.get('lunch').get('id') if daily_menu_data.get('lunch') else None
            daily_menu.dinner_id = daily_menu_data.get('dinner').get('id') if daily_menu_data.get('dinner') else None

            daily_menu_service.update(daily_menu)

        # Update menu
        menu_service.update(menu_id, name=name, favourite=favourite)

        return 'Menu {} updated'.format(menu_id)

api.add_resource(MenuApi, '/menus/<int:menu_id>')


class FavouriteMenuListApi(Resource):

    @marshal_with(menu_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all_by_favourites()

api.add_resource(FavouriteMenuListApi, '/menus/favourite')


class CurrentMenuListApi(Resource):

    @marshal_with(menu_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all_by_date(date.today())

api.add_resource(CurrentMenuListApi, '/menus/current')


def check_menu(menu_id, menu_service=MenuService()):
    menu = menu_service.get_by_id(menu_id)

    if not menu:
        abort(404, error='Menu {} does not exist'.format(menu_id))

    return menu


def check_daily_menu(menu_id, daily_menu_id, daily_menu_service=DailyMenuService()):
    daily_menu = daily_menu_service.get_by_menu_id_and_daily_menu_id(menu_id, daily_menu_id)

    if not daily_menu:
        abort(404, error='Daily Menu {} does not exist'.format(daily_menu_id))

    return daily_menu

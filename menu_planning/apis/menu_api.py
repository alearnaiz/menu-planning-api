from menu_planning import api
from flask_restful import Resource, marshal_with, abort
from flask import request
from menu_planning.actions.menu_generator import MenuGenerator
from menu_planning.services.daily_menu_service import DailyMenuService
from menu_planning.services.menu_service import MenuService
from menu_planning.services.starter_service import StarterService
from menu_planning.services.lunch_service import LunchService
from menu_planning.services.dinner_service import DinnerService
from menu_planning.apis.resources import menu_fields, menu_with_daily_menus_fields
from menu_planning.apis.utils import get_boolean, get_date, get_int, get_checkbox


class MenuListApi(Resource):

    @marshal_with(menu_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all()

    @marshal_with(menu_fields)
    def post(self):
        start_lunch = request.form.get('start_lunch')
        end_dinner = request.form.get('end_dinner')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not start_lunch or not end_dinner or not start_date or not end_date:
            abort(400, message='Wrong parameters')

        try:
            start_date = get_date(start_date)
            end_date = get_date(end_date)
            days = (end_date - start_date).days + 1

            menu_generator = MenuGenerator()
            menu = menu_generator.generate(days=days, start_date=start_date, start_lunch=get_boolean(start_lunch),
                                           end_dinner=get_boolean(end_dinner))

            name = request.form.get('name')
            favourite = request.form.get('favourite')

            if name and favourite:
                menu_service = MenuService()
                menu_service.update(menu.id, name=name, favourite=get_boolean(favourite))
            elif name:
                menu_service = MenuService()
                menu_service.update(menu.id, name=name)
            elif favourite:
                menu_service = MenuService()
                menu_service.update(menu.id, favourite=get_boolean(favourite))

        except Exception as exception:
            abort(400, message=str(exception))

        return menu, 201

api.add_resource(MenuListApi, '/menus')


class MenuApi(Resource):

    @marshal_with(menu_with_daily_menus_fields)
    def get(self, menu_id):
        menu_service = MenuService()
        menu = menu_service.get_by_id(menu_id)

        if not menu:
            abort(404, message="Menu {} doesn't exist".format(menu_id))

        starter_service = StarterService()
        lunch_service = LunchService()
        dinner_service = DinnerService()

        for daily_menu in menu.daily_menus:

            if daily_menu.lunch_id:
                lunch = lunch_service.get_by_id(daily_menu.lunch_id)
            else:
                lunch = None

            if daily_menu.starter_id:
                starter = starter_service.get_by_id(daily_menu.starter_id)
            else:
                starter = None

            if daily_menu.dinner_id:
                dinner = dinner_service.get_by_id(daily_menu.dinner_id)
            else:
                dinner = None

            daily_menu.starter = starter
            daily_menu.lunch = lunch
            daily_menu.dinner = dinner

        return menu

    def put(self, menu_id):
        menu_service = MenuService()
        menu = menu_service.get_by_id(menu_id)

        if not menu:
            abort(404, message="Menu {} doesn't exist".format(menu_id))

        # Update name and favourite
        name = request.form.get('name')
        favourite = get_boolean(request.form.get('favourite'))
        menu_service.update(menu_id, name=name, favourite=get_checkbox(favourite))

        # Update daily menus
        daily_menu_service = DailyMenuService()
        for daily_menu in menu.daily_menus:
            starter_id = get_int(request.form.get('starter[' + str(daily_menu.day) + ']'))
            lunch_id = get_int(request.form.get('lunch[' + str(daily_menu.day) + ']'))
            dinner_id = get_int(request.form.get('dinner[' + str(daily_menu.day) + ']'))

            daily_menu.starter_id = starter_id
            daily_menu.lunch_id = lunch_id
            daily_menu.dinner_id = dinner_id

            daily_menu_service.update(daily_menu)

        return 'Menu {} updated'.format(menu_id)

api.add_resource(MenuApi, '/menus/<int:menu_id>')


class MenuFavouriteListApi(Resource):

    @marshal_with(menu_fields)
    def get(self):
        menu_service = MenuService()
        return menu_service.get_all_by_favourites()

api.add_resource(MenuFavouriteListApi, '/menus/favourites')

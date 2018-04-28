from flask_restful import abort

from menu_planning.services.daily_menu_service import DailyMenuService
from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.food_service import FoodService
from menu_planning.services.lunch_service import LunchService
from menu_planning.services.menu_service import MenuService
from menu_planning.services.product_service import ProductService


class Validator:

    @staticmethod
    def check_menu(menu_id, menu_service=MenuService()):
        menu = menu_service.get_by_id(menu_id)

        if not menu:
            abort(404, error='Menu {} does not exist'.format(menu_id))

        return menu

    @staticmethod
    def check_product(product_id, product_service=ProductService()):
        product = product_service.get_by_id(product_id)

        if not product:
            abort(404, error='Product {} does not exist'.format(product_id))

        return product

    @staticmethod
    def check_lunch(lunch_id, lunch_service=LunchService()):
        lunch = lunch_service.get_by_id(id=lunch_id)
        if not lunch:
            abort(404, error='Lunch {} does not exist'.format(lunch_id))

        return lunch

    @staticmethod
    def check_food(food_id, food_service=FoodService()):
        food = food_service.get_by_id(id=food_id)
        if not food:
            abort(404, error='Food {} does not exist'.format(food_id))

        return food

    @staticmethod
    def check_dinner(dinner_id, dinner_service=DinnerService()):
        dinner = dinner_service.get_by_id(id=dinner_id)
        if not dinner:
            abort(404, error='Dinner {} does not exist'.format(dinner_id))

        return dinner

    @staticmethod
    def check_daily_menu(menu_id, daily_menu_id, daily_menu_service=DailyMenuService()):
        daily_menu = daily_menu_service.get_by_menu_id_and_daily_menu_id(menu_id, daily_menu_id)

        if not daily_menu:
            abort(404, error='Daily Menu {} does not exist'.format(daily_menu_id))

        return daily_menu

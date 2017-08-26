from menu_planning.models import DailyMenu
from menu_planning import db


class DailyMenuService:

    def create(self, day, menu_id, lunch_id, dinner_id, starter_id):
        daily_menu = DailyMenu(day, menu_id, lunch_id, dinner_id, starter_id)
        db.session.add(daily_menu)
        db.session.commit()
        return daily_menu

    def update(self, daily_menu):
        db.session.add(daily_menu)
        db.session.commit()
        return daily_menu

    def get_by_menu_id_and_daily_menu_id(self, menu_id, daily_menu_id):
        return DailyMenu.query.filter(DailyMenu.id == daily_menu_id, DailyMenu.menu_id == menu_id).first()

from menu_planning.models import Menu, DailyMenu
from menu_planning import db


class MenuService:

    def create(self, name=None, favourite=False):
        menu = Menu(name=name, favourite=favourite)
        db.session.add(menu)
        db.session.commit()
        return menu

    def get_by_id(self, id):
        return Menu.query.filter(Menu.id == id).first()

    def get_all(self):
        return Menu.query.all()

    def get_all_by_favourites(self):
        return Menu.query.filter(Menu.favourite.is_(True)).all()

    def get_all_by_date(self, date):
        query_dates = DailyMenu.query.filter(DailyMenu.day == date, DailyMenu.menu_id == Menu.id)
        return Menu.query.filter(query_dates.exists()).all()

    def update(self, id, name=None, favourite=False):
        menu = self.get_by_id(id)
        menu.name = name
        menu.favourite = favourite
        db.session.add(menu)
        db.session.commit()

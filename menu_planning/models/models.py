from menu_planning import db
from sqlalchemy.sql import func, expression
from enum import IntEnum


class FoodType(IntEnum):
    starter = 0
    lunch = 1
    dinner = 2


class ProductStatus(IntEnum):
    active = 0
    bought = 1


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    daily_menus = db.relationship('DailyMenu', lazy='select')
    favourite = db.Column(db.Boolean, server_default=expression.false())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, name=None, favourite=False):
        self.name = name
        self.favourite = favourite

    def __repr__(self):
        return 'Menu {0}, name {1}, created at {2}'.format(self.id, self.name, self.created_at)


class DailyMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    lunch_id = db.Column(db.Integer, db.ForeignKey('lunch.id'), nullable=True)
    dinner_id = db.Column(db.Integer, db.ForeignKey('dinner.id'), nullable=True)
    starter_id = db.Column(db.Integer, db.ForeignKey('starter.id'), nullable=True)

    def __init__(self, day, menu_id, lunch_id=None, dinner_id=None, starter_id=None):
        self.day = day
        self.menu_id = menu_id
        self.lunch_id = lunch_id
        self.dinner_id = dinner_id
        self.starter_id = starter_id

    def __repr__(self):
        return 'Daily menu {0}, day {1}'.format(self.id, self.day)


class FoodIngredient(db.Model):
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=True)

    def __init__(self, food_id, ingredient_id, quantity=None):
        self.food_id = food_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity

    def __repr__(self):
        return 'FoodIngredient, food {0}, ingredient {1}, quantity {2}'.format(self.food_id, self.ingredient_id,
                                                                               self.quantity)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return 'Food {0}, name {1}, type {2}'.format(self.id, self.name, self.type)


class Starter(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    food = db.relationship('Food', lazy='select')

    def __repr__(self):
        return 'Food {0}'.format(self.id)


class Lunch(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    days = db.Column(db.Integer, default=1)
    need_starter = db.Column(db.Boolean, server_default=expression.false())
    related_dinner_id = db.Column(db.Integer, db.ForeignKey('dinner.id'), nullable=True)
    food = db.relationship('Food', lazy='select')

    def __init__(self, days=1, need_starter=False, related_dinner_id=None):
        self.days = days
        self.need_starter = need_starter
        self.related_dinner_id = related_dinner_id

    def __repr__(self):
        return 'Lunch {0}, days {1}, need starter {2}, related dinner id {3}'.format(self.id, self.days,
                                                                                     self.need_starter,
                                                                                     self.related_dinner_id)


class Dinner(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    days = db.Column(db.Integer, default=1)
    related_lunch = db.relationship('Lunch', uselist=False, backref='related_dinner', lazy='select')
    food = db.relationship('Food', lazy='select')

    def __init__(self, days=1):
        self.days = days

    def __repr__(self):
        return 'Dinner {0}, days {1}'.format(self.id, self.days)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Ingredient {0}, name {1}'.format(self.id, self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=True)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, name, status, quantity=None):
        self.name = name
        self.quantity = quantity
        self.status = status

    def __repr__(self):
        return 'Product {0}, name {1}, quantity {2}, status {3}'.format(self.id, self.name, self.quantity, self.status)

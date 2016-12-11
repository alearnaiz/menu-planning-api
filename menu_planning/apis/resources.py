from flask_restful import fields


class DatetimeFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

starter_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute='food.name'),
}

dinner_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute='food.name'),
    'days': fields.Integer,
}

lunch_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute='food.name'),
    'days': fields.Integer,
}

daily_menu_fields = {
    'id': fields.Integer,
    'day': DatetimeFormat(),
    'starter': fields.Nested(starter_fields, allow_null=True),
    'lunch': fields.Nested(lunch_fields, allow_null=True),
    'dinner': fields.Nested(dinner_fields, allow_null=True),
}

menu_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'favourite': fields.Boolean,
    'created_at': DatetimeFormat(),
}

menu_with_daily_menus_fields = menu_fields.copy()
menu_with_daily_menus_fields['daily_menus'] = fields.List(fields.Nested(daily_menu_fields))

foods_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.Integer,
}

food_ingredient_fields = {
    'id': fields.Integer(attribute='ingredient_id'),
    'name': fields.String,
    'quantity': fields.Float,
}

food_with_ingredients_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'ingredients': fields.Nested(food_ingredient_fields),
}

ingredient_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'quantity': fields.Float,
    'status': fields.Integer,
}

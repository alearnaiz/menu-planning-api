from flask_restful import abort
from marshmallow import Schema, fields, validate, ValidationError

from menu_planning.models import ProductStatus


def validate_quantity(n):
    if n <= 0:
        raise ValidationError('Quantity must be greater than 0')


def validate_product_status(status):
    if status not in list(map(int, ProductStatus)):
        raise ValidationError('Status not valid')


class StarterSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True, allow_none=True)


class LunchSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    need_starter = fields.Bool(required=True)
    url = fields.Str(required=True, allow_none=True)
    related_dinner_id = fields.Integer(required=True, allow_none=True)
    days = fields.Integer(required=True)


class DinnerSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True, allow_none=True)
    days = fields.Integer(required=True)


class DailyMenuSchema(Schema):
    id = fields.Int(required=True)
    starter = fields.Nested(StarterSchema, required=True, many=False, allow_none=True)
    lunch = fields.Nested(LunchSchema, required=True, many=False, allow_none=True)
    dinner = fields.Nested(DinnerSchema, required=True, many=False, allow_none=True)


class MenuSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True, allow_none=True)
    favourite = fields.Bool(required=True, allow_none=True)
    daily_menus = fields.Nested(DailyMenuSchema, many=True,
                                validate=validate.Length(min=1, error='Field may not be an empty list'))


class IngredientSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


class ProductSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    quantity = fields.Float(required=True, allow_none=True, validate=validate_quantity)
    status = fields.Int(required=True, validate=validate_product_status)


class FoodIngredientSchema(Schema):
    ingredient = fields.Nested(IngredientSchema, many=False, required=True)
    quantity = fields.Float(required=True, allow_none=True, validate=validate_quantity)


def parser_request(request, schema):
    json_data = request.get_json()
    if not json_data:
        abort(400, error={'message': 'No input data provided'})
    data, errors = schema.load(json_data)
    if errors:
        abort(400, error=errors)
    return data


create_menu_schema = MenuSchema(exclude=('id', 'daily_menus'))
create_menu_schema.fields['start_lunch'] = fields.Bool(required=True)
create_menu_schema.fields['end_dinner'] = fields.Bool(required=True)
create_menu_schema.fields['start_date'] = fields.Date(required=True)
create_menu_schema.fields['end_date'] = fields.Date(required=True)
menu_with_daily_menus_schema = MenuSchema(only=(
    'name', 'favourite', 'daily_menus.id', 'daily_menus.starter.id', 'daily_menus.lunch.id', 'daily_menus.dinner.id')
)
starter_schema = StarterSchema(exclude=('id',))
lunch_schema = LunchSchema(exclude=('id',))
dinner_schema = DinnerSchema(exclude=('id',))
ingredient_schema = IngredientSchema(exclude=('id',))
product_schema = ProductSchema(exclude=('id',))
food_ingredient_schema = FoodIngredientSchema(many=True, only=('quantity', 'ingredient.id'))

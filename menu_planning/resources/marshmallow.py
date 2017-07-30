from flask_restful import abort
from marshmallow import Schema, fields, validate


class StarterSchema(Schema):
    id = fields.Int(required=True)


class LunchSchema(Schema):
    id = fields.Int(required=True)


class DinnerSchema(Schema):
    id = fields.Int(required=True)


class DailyMenuSchema(Schema):
    id = fields.Int(required=True)
    starter = fields.Nested(StarterSchema, many=False, allow_none=True)
    lunch = fields.Nested(LunchSchema, many=False, allow_none=True)
    dinner = fields.Nested(DinnerSchema, many=False, allow_none=True)


class MenuWithDailyMenusSchema(Schema):
    name = fields.Str(required=False, allow_none=True)
    favourite = fields.Bool(required=True)
    daily_menus = fields.Nested(DailyMenuSchema, many=True,
                                validate=validate.Length(min=1, error='Field may not be an empty list'))


def get_data(request, schema):
    data, errors = schema.load(request.get_json())
    if errors:
        abort(400, error=errors)
    return data


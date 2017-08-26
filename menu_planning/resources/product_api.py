from flask import request

from menu_planning import api, app
from flask_restful import Resource, abort, marshal_with

from menu_planning.models.schemas import product_schema, parser_request
from menu_planning.resources.output_fields import product_fields
from menu_planning.models import Product, ProductStatus
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.ingredient_service import IngredientService
from menu_planning.services.menu_service import MenuService
from menu_planning.services.product_service import ProductService


class ProductListApi(Resource):

    @marshal_with(product_fields)
    def get(self):
        product_service = ProductService()
        return product_service.get_all()

    def delete(self):
        product_service = ProductService()
        product_service.delete_all()
        return 'Products deleted', 201

    @marshal_with(product_fields)
    def post(self):
        name, quantity, status = check_request()

        product = set_product(name=name, quantity=quantity, status=status)

        product_service = ProductService()
        product = product_service.create(product)
        return product, 201

api.add_resource(ProductListApi, '/products')


class ProductApi(Resource):

    def put(self, product_id):
        product_service = ProductService()

        check_product(product_id, product_service)

        name, quantity, status = check_request()
        product = set_product(name=name, quantity=quantity, status=status, id=product_id)

        product_service.update(product)
        return 'Product {} updated'.format(product_id)

    def delete(self, product_id):
        product_service = ProductService()

        product = check_product(product_id, product_service)

        product_service.delete(product)
        return 'Product {} deleted'.format(product_id)

api.add_resource(ProductApi, '/products/<int:product_id>')


@app.route('/menus/<int:menu_id>/ingredients/products', methods=['GET'])
def send_ingredients_from_menu_to_grocery_list(menu_id):

    menu_service = MenuService()
    menu = menu_service.get_by_id(menu_id)

    if not menu:
        return 'Menu {} does not exist'.format(menu_id), 404

    food_ingredient_service = FoodIngredientService()
    food_ingredients = food_ingredient_service.get_all_by_menu_id(menu_id=menu_id)
    ingredient_service = IngredientService()

    products = {}
    for food_ingredient in food_ingredients:
        if food_ingredient.ingredient_id not in products.keys():
            ingredient = ingredient_service.get_by_id(food_ingredient.ingredient_id)
            product = Product(name=ingredient.name, status=ProductStatus.active.value, quantity=food_ingredient.quantity)
            products[food_ingredient.ingredient_id] = product
        else:
            if food_ingredient.quantity:
                product = products[food_ingredient.ingredient_id]
                if product.quantity:
                    product.quantity += food_ingredient.quantity
                else:
                    product.quantity = food_ingredient.quantity

    if products:
        product_service = ProductService()
        for ingredient_id in products:
            product = products[ingredient_id]
            product_service.create(product)

    return 'Ingredients from menu {} sent to the grocery list'.format(menu_id), 201


def set_product(name, quantity, status, id=None):
    product = Product(name=name, quantity=quantity, status=status)

    if id:
        product.id = id

    return product


def check_product(product_id, product_service=ProductService()):
    product = product_service.get_by_id(product_id)

    if not product:
        abort(404, error='Product {} does not exist'.format(product_id))

    return product


def check_request():
    # Request
    parser = parser_request(request, product_schema)
    name = parser.get('name')
    quantity = parser.get('quantity')
    status = parser.get('status')

    return name, quantity, status

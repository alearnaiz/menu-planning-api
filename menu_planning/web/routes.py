from flask import render_template, request, jsonify, send_from_directory

from menu_planning import app
from menu_planning.resources import menu_api, starter_api, dinner_api, lunch_api, food_api, food_ingredient_api, ingredient_api, product_api


@app.route('/web', methods=['GET'])
def current_menus():
    menu_list = menu_api.CurrentMenuListApi().get()

    menus = list()
    for menu in menu_list:
        menus.append(menu_api.MenuApi().get(menu['id']))

    return render_template('current-menus.html', menus=menus)


@app.route('/web/next', methods=['GET'])
def next_menus():
    menu_list = menu_api.NextMenuListApi().get()

    menus = list()
    for menu in menu_list:
        menus.append(menu_api.MenuApi().get(menu['id']))

    return render_template('next-menus.html', menus=menus)


@app.route('/web/favourites', methods=['GET'])
def favourite_menus():
    menu_list = menu_api.FavouriteMenuListApi().get()

    menus = list()
    for menu in menu_list:
        menus.append(menu_api.MenuApi().get(menu['id']))

    return render_template('favourite-menus.html', menus=menus)


@app.route('/web/all-menus', methods=['GET'])
def all_menus():
    menu_list = menu_api.MenuListApi().get()

    menus = list()
    for menu in menu_list:
        menus.append(menu_api.MenuApi().get(menu['id']))

    return render_template('all-menus.html', menus=menus)


@app.route('/web/menu/<int:menu_id>', methods=['GET'])
def show_menu(menu_id):
    menu = menu_api.MenuApi().get(menu_id)

    return render_template('show-menu.html', menu=menu)


@app.route('/web/create-menu', methods=['GET', 'POST'])
def create_menu():
    if request.method == 'GET':
        return render_template('create-menu.html')
    else:
        response = menu_api.MenuListApi().post()
        return jsonify(response[0])


@app.route('/web/edit-menu/<int:menu_id>', methods=['GET', 'PUT'])
def edit_menu(menu_id):
    if request.method == 'GET':
        menu = menu_api.MenuApi().get(menu_id)

        starters = starter_api.StarterListApi().get()
        dinners = dinner_api.DinnerListApi().get()
        lunches = lunch_api.LunchListApi().get()

        return render_template('edit-menu.html', menu=menu, starters=starters, dinners=dinners, lunches=lunches)
    else:
        response = menu_api.MenuApi().put(menu_id)
        return jsonify(response[0])


@app.route('/web/foods', methods=['GET'])
def show_foods():
    foods = food_api.FoodListApi().get()
    starters = []
    lunches = []
    dinners = []

    for food in foods:
        if food["type"] == 0:
            starters.append(food)
        elif food["type"] == 1:
            lunches.append(food)
        elif food["type"] == 2:
            dinners.append(food)

    return render_template('foods.html', starters=starters, lunches=lunches, dinners=dinners)


@app.route('/web/food/<int:food_id>', methods=['GET'])
def show_food(food_id):
    food = food_api.FoodApi().get(food_id)
    lunch = None
    dinner = None
    related = None
    if food["type"] == 1:
        lunch = lunch_api.LunchApi().get(food_id)
        if lunch["related_dinner_id"]:
            related = food_api.FoodApi().get(lunch["related_dinner_id"])
    elif food["type"] == 2:
        dinner = dinner_api.DinnerApi().get(food_id)
        if dinner["related_lunch_id"]:
            related = food_api.FoodApi().get(dinner["related_lunch_id"])

    return render_template('show-food.html', food=food, lunch=lunch, dinner=dinner, related=related)


@app.route('/web/ingredient', methods=['GET', 'POST'])
def create_ingredient():
    if request.method == 'GET':
        return render_template('create-ingredient.html')
    else:
        response = ingredient_api.IngredientListApi().post()
        return jsonify(response[0])


@app.route('/web/ingredients', methods=['GET'])
def show_ingredients():
    ingredients = ingredient_api.IngredientListApi().get()
    return render_template('ingredients.html', ingredients=ingredients)


@app.route('/web/food/<int:food_id>/ingredients', methods=['GET', 'PUT'])
def edit_food_ingredients(food_id):
    if request.method == 'GET':
        food = food_api.FoodApi().get(food_id)
        lunch = None
        dinner = None
        related = None
        if food["type"] == 1:
            lunch = lunch_api.LunchApi().get(food_id)
            if lunch["related_dinner_id"]:
                related = food_api.FoodApi().get(lunch["related_dinner_id"])
        elif food["type"] == 2:
            dinner = dinner_api.DinnerApi().get(food_id)
            if dinner["related_lunch_id"]:
                related = food_api.FoodApi().get(dinner["related_lunch_id"])

        ingredients = ingredient_api.IngredientListApi().get()
        return render_template('edit-food-ingredients.html', food=food, ingredients=ingredients, lunch=lunch, dinner=dinner, related=related)
    else:
        response = food_ingredient_api.FoodIngredientListApi().put(food_id)
        return jsonify(response[0])


@app.route('/web/template-ingredient', methods=['GET'])
def get_template_add_ingredient():
    ingredients = ingredient_api.IngredientListApi().get()
    return render_template('utils/add-ingredient.html', ingredients=ingredients)


@app.route('/web/create-food', methods=['GET'])
def create_food():
    return render_template('create-food.html')


@app.route('/web/create-starter', methods=['GET', 'POST'])
def create_start():
    if request.method == 'GET':
        return render_template('create-starter.html')
    else:
        response = starter_api.StarterListApi().post()
        return jsonify(response[0])


@app.route('/web/create-lunch', methods=['GET', 'POST'])
def create_lunch():
    if request.method == 'GET':
        dinners = dinner_api.DinnerListApi().get()
        return render_template('create-lunch.html', dinners=dinners)
    else:
        response = lunch_api.LunchListApi().post()
        return jsonify(response[0])


@app.route('/web/create-dinner', methods=['GET', 'POST'])
def create_dinner():
    if request.method == 'GET':
        return render_template('create-dinner.html')
    else:
        response = dinner_api.DinnerListApi().post()
        return jsonify(response[0])


@app.route('/web/grocery-list', methods=['GET', 'POST', 'DELETE'])
def my_products():
    if request.method == 'GET':
        products = product_api.ProductListApi().get()
        return render_template('grocery-list.html', products=products)
    elif request.method == 'DELETE':
        response = product_api.ProductListApi().delete()
        return jsonify(response[0])
    else:
        response = product_api.ProductListApi().post()
        return jsonify(response[0])


@app.route('/web/template-product', methods=['GET'])
def get_template_add_product():
    return render_template('utils/add-product.html')


@app.route('/web/edit-product/<int:product_id>', methods=['PUT', 'DELETE'])
def edit_product(product_id):
    if request.method == 'PUT':
        response = product_api.ProductApi().put(product_id)
        return jsonify(response[0])
    else:
        response = product_api.ProductApi().delete(product_id)
        return jsonify(response[0])


@app.route('/web/send-products/<int:menu_id>', methods=['GET'])
def send_product_to_grocery_list(menu_id):
    response = product_api.send_ingredients_from_menu_to_grocery_list(menu_id)
    return jsonify(response[0])


@app.route('/web/manifest.json')
def get_manifest():
    return send_from_directory('web/manifest', 'manifest.json')


@app.route('/web/manifest/icon.png')
def get_manifest_icon():
    return send_from_directory('web/manifest', 'icon.png')

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os
from flask_cors import CORS
app = Flask(__name__)
api = Api(app)
with open(os.getcwd() + '/credentials.json') as data_file:
    data = json.load(data_file)['mysql']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}?charset={4}'\
    .format(data['user'], data['password'], data['host'], data['database'], data['charset'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
migrate = Migrate(app, db)

import menu_planning.resources.menu_api
import menu_planning.resources.food_api
import menu_planning.resources.ingredient_api
import menu_planning.resources.product_api
import menu_planning.resources.starter_api
import menu_planning.resources.lunch_api
import menu_planning.resources.dinner_api
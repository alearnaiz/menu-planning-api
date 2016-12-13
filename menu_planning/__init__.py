from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
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

import menu_planning.apis.menu_api
import menu_planning.apis.food_api
import menu_planning.apis.ingredient_api
import menu_planning.apis.product_api
import menu_planning.apis.starter_api
import menu_planning.apis.lunch_api
import menu_planning.apis.dinner_api
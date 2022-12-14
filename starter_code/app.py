import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT


from starter_code.resources.store import Store, StoreList
from starter_code.resources.item import Item, ItemList
from starter_code.resources.user import UserRegister
from starter_code.security import authenticate, identity

app = Flask(__name__)

app.config['DEBUG'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

file_path = os.path.abspath(os.getcwd()) + "/instance/data.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path


api = Api(app)

app.secret_key = "jose123"

# creates the /auth endpoint
jwt = JWT(app, authenticate, identity)
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

api.add_resource(UserRegister, "/register")

# @app.errorhandler(JWT)
def auth_error_handler():
    return jsonify({"message": "Unauthorized, please include an authorization header"}), 401


if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)

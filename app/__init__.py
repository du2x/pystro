from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy


from app.config import Config
from app.auth import authenticate, identity
from app.resources.user import UserAPI, UsersAPI

def set_api_routes(api):
    api.add_resource(UsersAPI, '/users', endpoint='users')
    api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')    

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_envvar('SMARTLUNCH_SETTINGS', silent=True)
    db = SQLAlchemy(app)    
    migrate = Migrate(app, db)
    api = Api(app)
    set_api_routes(api)
    JWT(app, authenticate, identity)
    return app, db


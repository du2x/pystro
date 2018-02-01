from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

from app.resources.user import UserAPI, UsersAPI
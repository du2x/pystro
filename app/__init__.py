from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt import JWT


from app.config import Config
from app.models import db
from app.auth import authenticate, identity

app = Flask(__name__)
app.config.from_object(Config)
app.config.from_envvar('SMARTLUNCH_SETTINGS', silent=True)

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
JWT(app, authenticate, identity)

from app.resources.user import UserAPI, UsersAPI
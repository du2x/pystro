from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate

from .config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

api = Api(app)
db = SQLAlchemy(app)
db.create_all()

migrate = Migrate(app, db)

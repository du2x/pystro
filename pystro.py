""" boots up pystro app """
from flask import render_template
from flask_migrate import Migrate, upgrade

from api import create_app
from api.database import db
from api import init_api_data
from api.models.user import User
from api.models.restaurant import Restaurant


app = create_app()
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('src/index.html')


@app.shell_context_processor
def make_shell_context():
    """ initializes vars for flask shell """
    return dict(db=db, User=User, Restaurant=Restaurant)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
    # creates initial data
    init_api_data(app)

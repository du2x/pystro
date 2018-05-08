""" boots up pystro app """
from flask import render_template, make_response, current_app
from flask_migrate import Migrate, upgrade
from flask_cors import CORS

from api import create_app
from api.database import db
from api import init_api_data
from api.models.user import User
from api.models.restaurant import Restaurant


app = create_app(debug=True)
CORS(app)


def setup_spa_route(app):
    app.static_folder='../smartlunch-client'
    app.template_folder='../smartlunch-client/src'
    app.static_url_path=''

    @app.route('/')
    def index():
        return make_response(render_template('index.html'))


@app.shell_context_processor
def make_shell_context():
    """ initializes vars for flask shell """
    return dict(app=app, db=db, User=User, Restaurant=Restaurant)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
    # creates initial data
    init_api_data(app)

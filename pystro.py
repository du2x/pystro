""" boots up pystro app """
from flask_migrate import Migrate, upgrade

from application import create_app
from application.database import db
from application import init_api_data
from application.models.user import User
from application.models.restaurant import Restaurant


app = create_app()
migrate = Migrate(app, db)


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

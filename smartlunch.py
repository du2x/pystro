from application import create_app
from flask_migrate import Migrate

app, db = create_app()
migrate = Migrate(app, db)

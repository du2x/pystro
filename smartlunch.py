from application import create_app
from flask_jwt import jwt_required



app, db = create_app()
app.run()
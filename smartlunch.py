from app import create_app
from flask_jwt import jwt_required


app, db = create_app()
db.drop_all()
db.create_all()
app.run()

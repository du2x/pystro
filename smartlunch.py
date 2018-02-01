from app import app, api
from flask_jwt import jwt_required


@app.route('/')
@jwt_required()
def index():
    return "Hello, World!"

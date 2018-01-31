from app import app, api
from app.resources.user import UsersAPI

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

api.add_resource(UsersAPI, '/users', endpoint='user')


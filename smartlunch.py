from app import app, api
import auth

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


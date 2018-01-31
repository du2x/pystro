from app import app, api

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"



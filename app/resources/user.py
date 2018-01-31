"""
    Defines APIs for user handling.
"""
from flask import request, jsonify
from flask_restful import Resource, reqparse
from app.models.user import User, Role
from .. import db
from .. import api

"""
    Defines routes for users listing and user adding.
"""
class UsersAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, required = True,
            help = 'No name provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
            help = 'No password provided', location = 'json')            
        self.reqparse.add_argument('email', type = str, required = True,
            help = 'No email provided', location = 'json')                        
        super(UsersAPI, self).__init__()

    def post(self):
        data = request.get_json()
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return "User " + user.username + " has been saved", 201

    def get(self):
        users = User.find_all()
        if users:
            return jsonify(users)
        else:
            return [], 200


"""
    Defines routes for user editing and user viewing.
"""
class UserAPI(Resource):
    pass

api.add_resource(UsersAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')

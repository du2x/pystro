"""
This module implements authentication and authorization features
"""
from flask import abort
from flask_jwt import JWT, jwt_required, current_identity
from app.models.user import User
from app import app
from functools import wraps

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

def hasrole(argument):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if argument in current_identity.roles: 
                return function(*args, **kwargs)
            return abort(401)
        return wrapper
    return real_decorator

JWT(app, authenticate, identity)

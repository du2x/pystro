"""
This module implements authentication and authorization features
"""
from flask import abort
from flask_jwt import current_identity
from application.models.user import User


def authenticate(email, password):
    user = User.find_by_email(email)
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.find_by_id(user_id)
    return user


def is_admin(function):
    def wrapper(*args, **kwargs):
        if current_identity.is_admin:
            return function(*args, **kwargs)
        return abort(401)


def is_manager(function):
    def wrapper(*args, **kwargs):
        if current_identity.is_admin or current_identity.is_manager:
            return function(*args, **kwargs)
        return abort(401)


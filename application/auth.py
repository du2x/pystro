"""
This module implements authentication and authorization features
"""
from functools import wraps

from flask import abort
from flask_jwt import current_identity, _jwt_required, jwt_required
from application.models.user import User


def authenticate(email, password):
    user = User.find_by_email(email)
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.find_by_id(user_id)
    return user


authenticated_user = jwt_required


def only_admin():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(None)
            if current_identity.is_admin:
                return fn(*args, **kwargs)
            return abort(403)
        return decorator
    return wrapper


def only_manager():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(None)
            if current_identity.is_admin or current_identity.is_manager:
                return fn(*args, **kwargs)
            return abort(403)
        return decorator
    return wrapper

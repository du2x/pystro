"""
This module implements authentication and authorization features
"""
from functools import wraps

from flask import abort
from flask_jwt import current_identity, _jwt_required

from .models.user import User
from .utils import get_current_restaurant


def authenticate(email, password):
    user = User.find_by_email(email)
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.find_by_id(user_id)
    return user


def authenticated_user():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(None)
            if current_identity.is_activated():
                return fn(*args, **kwargs)
            return abort(403)
        return decorator
    return wrapper


def only_admin():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(None)
            if current_identity.is_activated() and current_identity.is_admin:
                return fn(*args, **kwargs)
            return abort(403)
        return decorator
    return wrapper


def only_manager():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(None)
            restaurant = get_current_restaurant()            
            if current_identity.is_activated() and \
                    ((current_identity.is_admin) or
                     current_identity.is_manager_of(restaurant)):
                return fn(*args, **kwargs)
            return abort(403)
        return decorator
    return wrapper

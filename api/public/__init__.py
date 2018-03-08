"""
This packages defines the resources for the
managing restaurants and users
"""
from .user import UserAPI, UsersAPI, ResetPasswordAPI


def setup_public_api_routes(api):
    api.add_resource(UsersAPI, '/users', endpoint='users')
    api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')
    api.add_resource(ResetPasswordAPI, '/resetpassword', endpoint='resetpw')


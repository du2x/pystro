"""
    Defines APIs for user handling.
"""
from flask import current_app
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError

import jwt

from api.models.user import User
from api.database import db
from api.auth import only_admin, authenticated_user
from api.auth import current_identity
from api.email import send_email


nameArg = reqparse.Argument(name='name', type=str,
                            required=False,
                            help='name of user',
                            location='json')
phoneArg = reqparse.Argument(name='phone', type=str,
                             required=False,
                             help='phone of user',
                             location='json')
emailArg = reqparse.Argument(name='email', type=str,
                             required=True,
                             help='No email provided',
                             location='json')
pwdArg = reqparse.Argument(name='password', type=str,
                           required=True,
                           help='No password provided',
                           location='json')
admArg = reqparse.Argument(name='is_admin', type=bool,
                           required=False,
                           help='If user is admin',
                           location='json')
tokArg = reqparse.Argument(name='activation_token', type=str,
                           required=True,
                           help='Activation token',
                           location='json')


class UsersAPI(Resource):
    """
    Defines routes for users listing and user adding.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def post(self):
        self.reqparse.add_argument(emailArg)
        data = self.reqparse.parse_args()
        if User.find_by_email(data['email']):
            return 'Email already in use.', 203
        user = User(email=data['email'])
        try:
            db.session.add(user)
            db.session.commit()
            activation_token = jwt.encode(
                            {'user_email': data['email']},
                            current_app.config['JWT_SECRET_KEY'],
                            current_app.config['JWT_ALGORITHM']).decode("utf-8")     
            send_email('Complete yor registration on Pystro.', data['email'],
                       'Clique em base_url/?token='+activation_token)
            return user.serializable(), 201
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400

    def put(self):
        self.reqparse.add_argument(emailArg)
        self.reqparse.add_argument(nameArg)
        self.reqparse.add_argument(phoneArg)
        self.reqparse.add_argument(pwdArg)
        self.reqparse.add_argument(admArg)
        self.reqparse.add_argument(tokArg)
        data = self.reqparse.parse_args()
        try:
            user = User.find_by_email(data['email'])
            token = str(jwt.encode(
                            {'user_email': data['email']},
                                current_app.config['JWT_SECRET_KEY'],
                                current_app.config['JWT_ALGORITHM']))
            if not user:
                return "User not created yet.", 402
            if not user.is_activated():
                if 'activation_token' not in data.keys() or \
                        not data['activation_token']:
                    return 'token not sent.', 401
                if not user.activate(data['activation_token']):
                    return 'token is invalid.', 403
            password = data['password']
            del(data['password'])
            del(data['activation_token'])
            for key in data.keys():
                setattr(user, key, data[key])
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400
        return "User " + user.email + " has been saved", 200

    @only_admin()
    def get(self):
        return User.find_all()


class UserAPI(Resource):
    """
    Defines routes for user editing and user viewing.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(nameArg)
        self.reqparse.add_argument(phoneArg)
        self.reqparse.add_argument(admArg)

        super(UserAPI, self).__init__()

    @authenticated_user()
    def get(self, id):
        user = User.find_by_id(id)
        if not user:
            return "User not found", 404
        elif current_identity.id != id  \
                and not current_identity.is_admin:
            return "Forbidden", 403
        else:
            return user.serializable(), 200

    @authenticated_user()
    def put(self, id):
        user = User.find_by_id(id)
        if not user:
            return "User not found", 404
        elif current_identity.id != id  \
                and not current_identity.is_admin:
            return "Forbidden", 403
        else:
            data = self.reqparse.parse_args()
            for k, v in data.items():
                setattr(user, k, v)
            db.session.add(user)
            db.session.commit()
            return user.serializable(), 200


resetTokArg = reqparse.Argument(name='reset_pw_token', type=str,
                                required=True,
                                help='Reset password token',
                                location='json')


class ResetPasswordAPI(Resource):
    """
    Defines route for remeber password feature.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(ResetPasswordAPI, self).__init__()

    def put(self):
        """
        Request for reset password
        """
        self.reqparse.add_argument(emailArg)
        data = self.reqparse.parse_args()
        user = User.find_by_email(data['email'])
        if not user:
            return "User not found", 404
        if not user.is_activated():     
            return "User is not activated yet.", 403        
        token = jwt.encode(
                           {'user_email': data['email']},
                            current_app.config['JWT_SECRET_KEY'],
                            current_app.config['JWT_ALGORITHM']).decode('utf-8')
        user.reset_pw_token = token
        try:
            db.session.add(user)
            db.session.commit()
            send_email('Reset your password on Pystro.', data['email'],
                       'Clique em base_url/?token='+token)

        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400

    def post(self):
        """
        Request for seting new password
        """
        self.reqparse.add_argument(pwdArg)
        self.reqparse.add_argument(emailArg)
        self.reqparse.add_argument(resetTokArg)
        data = self.reqparse.parse_args()
        try:
            user = User.find_by_email(data['email'])
            if data['reset_pw_token'] != user.reset_pw_token:
                return 403
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400

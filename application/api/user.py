"""
    Defines APIs for user handling.
"""
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from sqlalchemy.exc import IntegrityError

from application.models.user import User
from application.database import db

usernameArg = reqparse.Argument(name='username', type=str,
                                required=True,
                                help='No name provided',
                                location='json')
emailArg = reqparse.Argument(name='email', type=str,
                             required=True,
                             help='No email provided',
                             location='json')
pwdArg = reqparse.Argument(name='password', type=str,
                           required=True,
                           help='No password provided',
                           location='json')


class UsersAPI(Resource):
    """
    Defines routes for users listing and user adding.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(usernameArg)
        self.reqparse.add_argument(emailArg)
        self.reqparse.add_argument(pwdArg)
        super(UsersAPI, self).__init__()

    def post(self):        
        data = self.reqparse.parse_args()  
        try:
            user = User(username=data['username'])
            user.set_password(data['password'])        
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400
        return "User " + user.username + " has been saved", 201

    @jwt_required()
    def get(self):
        users = User.find_all()
        if users:
            return users, 200
        else:
            return [], 200


class UserAPI(Resource):
    """
    Defines routes for user editing and user viewing.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(usernameArg)
        self.reqparse.add_argument(emailArg)
        super(UserAPI, self).__init__()

    def get(self, id):
        user = User.find_by_id(id)
        if not user:
            return "User not found", 404
        else:
            return user.serializable(), 200

    def put(self, id):
        user = User.find_by_id(id)        
        if not user:
            return "User not found", 404
        else:
            data = self.reqparse.parse_args()            
            user.username = data['username']
            user.email = data['email']
            db.session.add(user)
            db.session.commit()
            return user, 200
            # todo: roles

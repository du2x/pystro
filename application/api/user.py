"""
    Defines APIs for user handling.
"""
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from sqlalchemy.exc import IntegrityError

from application.models.user import User
from application.database import db
from application.auth import only_manager, only_admin


emailArg = reqparse.Argument(name='email', type=str,
                             required=True,
                             help='No email provided',
                             location='json')
pwdArg = reqparse.Argument(name='password', type=str,
                           required=True,
                           help='No password provided',
                           location='json')
mngArg = reqparse.Argument(name='is_manager', type=bool,
                           required=False,
                           help='If user is manager',
                           location='json')


class UsersAPI(Resource):
    """
    Defines routes for users listing and user adding.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(emailArg)
        self.reqparse.add_argument(pwdArg)
        self.reqparse.add_argument(mngArg)        
        super(UsersAPI, self).__init__()

    def post(self):        
        data = self.reqparse.parse_args()  
        try:
            user = User(email=data['email'], is_manager=data['is_manager'])
            user.set_password(data['password'])        
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400
        return "User " + user.email + " has been saved", 201

    @jwt_required()
    @only_manager()    
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
            user.email = data['email']
            db.session.add(user)
            db.session.commit()
            return user, 200
            # todo: roles

"""
    Defines APIs for user handling.
"""
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError

from application.models.user import User
from application.database import db
from application.auth import only_admin, authenticated_user
from application.auth import current_identity


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
mngArg = reqparse.Argument(name='is_manager', type=bool,
                           required=False,
                           help='If user is manager',
                           location='json')
admArg = reqparse.Argument(name='is_admin', type=bool,
                           required=False,
                           help='If user is admin',
                           location='json')


class UsersAPI(Resource):
    """
    Defines routes for users listing and user adding.
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(nameArg)
        self.reqparse.add_argument(phoneArg)
        self.reqparse.add_argument(emailArg)
        self.reqparse.add_argument(pwdArg)
        self.reqparse.add_argument(mngArg)
        self.reqparse.add_argument(admArg)
        super(UsersAPI, self).__init__()

    def post(self):
        data = self.reqparse.parse_args()
        try:
            password = data['password']
            del(data['password'])
            user = User(**data)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return "Integrity error: " + str(e), 400
        return "User " + user.email + " has been saved", 201

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
        self.reqparse.add_argument(mngArg)
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

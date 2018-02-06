from werkzeug.security import generate_password_hash, check_password_hash
from application.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean(), default=False)
    is_manager = db.Column(db.Boolean(), default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_role(self, role):
        if not self.has_role(role):
            self.roles.append(role)

    def serializable(self):
        return {'id': self.id,
                'username': self.username,
                'email': self.email}

    @classmethod
    def find_by_id(cls, uid):
        result = cls.query.filter(cls.id == uid)
        if result.count() == 1:
            return result.first()
        return None

    @classmethod
    def find_by_username(cls, username):
        result = cls.query.filter(cls.username == username)
        if result.count() == 1:
            return result.first()
        return None

    @classmethod
    def find_all(cls):
        return [user.serializable() for user in cls.query.all()]

    def __repr__(self):
        return '<User {} ({})>'.format(self.username, self.email)

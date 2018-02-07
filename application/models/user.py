from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from application.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(140), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                        onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=True)
    profile_url = db.Column(db.String, nullable=True)
    access_token = db.Column(db.String, nullable=True)    
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
                'email': self.email}

    @classmethod
    def find_by_id(cls, uid):
        result = cls.query.filter(cls.id == uid)
        if result.count() == 1:
            return result.first()
        return None

    @classmethod
    def find_by_email(cls, email):
        result = cls.query.filter(cls.email == email)
        if result.count() == 1:
            return result.first()
        return None

    @classmethod
    def find_all(cls):
        return [user.serializable() for user in cls.query.all()]

    def __repr__(self):
        return '<User {}>'.format(self.email)

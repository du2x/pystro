
import base64
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app

import jwt

from application.database import db
from application.models import BaseModel
from application.models.restaurant import Restaurant
from application.models.restaurant import restaurants_managers


class User(BaseModel):
    email = db.Column(db.String(140), index=True, unique=True)
    name = db.Column(db.String(140), index=True)
    phone = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    activated_on = db.Column(db.DateTime)
    name = db.Column(db.String(140), nullable=True)
    profile_url = db.Column(db.String(220), nullable=True)
    reset_pw_token = db.Column(db.String(70), nullable=True)
    is_admin = db.Column(db.Boolean(), default=False)
    manages = db.relationship("Restaurant",
                              secondary=restaurants_managers,
                              back_populates='managers')

    def is_activated(self):
        return self.activated_on is not None

    def is_manager_of(self, restaurant):
        return restaurant.id in [rst.id
                              for rst in self.manages]

    def activate(self, token):
        if self.is_activated():
            return True
        try:
            user_email = jwt.decode(token,
                                    current_app.config['JWT_SECRET_KEY'],
                                    algorithms=current_app.config['JWT_ALG']
                                    )['user_email']
            if user_email == self.email:
                self.activated_on = datetime.utcnow()
                return True
        except jwt.ExpiredSignature:
            # TODO: log this
            return False
        except jwt.InvalidTokenError:
            # TODO: log this
            return False
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serializable(self):
        return {'id': self.id,
                'name': self.name,
                'email': self.email}

    @classmethod
    def find_by_email(cls, email):
        result = cls.query.filter(cls.email == email)
        if result.count() == 1:
            return result.first()
        return None

    def __repr__(self):
        return '<User {}>'.format(self.email)

import os
from datetime import datetime

from flask import Flask
from flask_jwt import JWT
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import ObjectDeletedError

from api.auth import authenticate, identity
from api.database import db
from api.config import defaultconfig
from api.models.user import User
from api.models.menu import Item, Section
from api.models.restaurant import Restaurant
from api.admin import setup_admin_api_routes
from api.public import setup_public_api_routes
from api.restaurants import register_restaurants_blueprints


def create_app(pconfig=None, debug=False):
    app = Flask(__name__)
    app.debug = debug
    configobj = pconfig or \
        os.environ.get('PYSTRO_SETTINGS') or \
        defaultconfig
    app.config.from_object(configobj)
    app.app_context().push()
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        try:
            db.create_all()
            if not app.testing:
                init_api_data(app)
        except (OperationalError, ObjectDeletedError):
            db.session.rollback()
            db.session.remove()
    setup_admin_api_routes(app)
    setup_public_api_routes(app)
    JWT(app, authenticate, identity)
    register_restaurants_blueprints(app)
    return app


def init_api_data(app):
    """ sets up api initial data """
    dummy_password = '123'
    try:
        u1 = User(email='john@example.com', is_admin=True)
        u1.set_password(dummy_password)
        u1.activated_on = datetime.utcnow()
        u2 = User(email='susan@example.com')
        u2.set_password(dummy_password)
        u2.activated_on = datetime.utcnow()
        u3 = User(email='karl@example.com')
        u3.set_password(dummy_password)
        u3.activated_on = datetime.utcnow()
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()
        db.session.flush()
        rest = Restaurant(name='Almazen', cname='almazen')
        rest.managers.append(u3)
        db.session.add(rest)
        db.session.commit()
        db.session.flush()
        s1 = Section(title='Food', description='Our delicious food.',
                     created_by=u1.id, restaurant_id=rest.id)
        s2 = Section(title='Drinks', description='Our stunning drinks.',
                     created_by=u1.id, restaurant_id=rest.id)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        db.session.flush()
        i1 = Item(title='Acabaxi', description='A great abacaxi. Very big.',
                  created_by=u1.id, price=10, section_id=s1.id, restaurant_id=rest.id)
        i2 = Item(title='Banana', description='A great bannanana. Very big.',
                  created_by=u1.id, price=15, section_id=s1.id, restaurant_id=rest.id)
        db.session.add(i1)
        db.session.add(i2)
        db.session.commit()
        return {
            'RESTAURANT_ID': rest.id,
            'RESTAURANT_CNAME': rest.cname,
            'ITEM_ID': i1.id,
            'SECTION_ID': s1.id,
            'USER_ADMIN_EMAIL': u1.email,
            'USER_ADMIN_PASSWORD': dummy_password,
            'USER_COMMON_EMAIL': u2.email,
            'USER_COMMON_PASSWORD': dummy_password,
            'USER_MANAGER_EMAIL': u3.email,
            'USER_MANAGER_PASSWORD': dummy_password
        }
    except IntegrityError:
        db.session.rollback()
        db.session.remove()
        return None

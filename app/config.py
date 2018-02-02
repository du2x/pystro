import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    JWT_SECRET_KEY = 'super-secret'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'smartlunch.db')
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


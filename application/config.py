import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = 'super-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    # ...
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'smartlunch_dev.db')



class TestConfig(Config):
    # ...    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'



class ProductionConfig(object):
    # ...
    JWT_SECRET_KEY = 'super-really-secret'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')    


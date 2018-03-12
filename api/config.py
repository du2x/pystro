import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = 'super-secret'
    JWT_ALG = 'HS256'
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600) # one hour
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USERNAME = None
    MAIL_PASSWORD = None    
    MAIL_SENDER = 'support@pystro.com'        
    


class DevelopmentConfig(Config):
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pystro.db'


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class HerokuConfig(Config):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pystro.db'


class ProductionConfig(object):
    JWT_SECRET_KEY = 'super-really-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


defaultconfig = DevelopmentConfig

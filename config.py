"""Default Application Configuration"""
import os

class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = "WataGwanistA"
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

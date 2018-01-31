import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	SECRET_KEY = "justtest"

class DevConfig(BaseConfig):
	DEBUG  = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'DevData.sqlite')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
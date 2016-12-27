import os

basedir = os.path.abspath(os.path.dirname(__file__))

GOOGLE_CLIENT_ID = '454289862376-ue1c1285rcpg0bsv837unipumimaurg0.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '_ymiPkiaMnws2o6x19cQrNx2'

REDIRECT_URI = '/oauth2callback'

SECRET_KEY = 'development key'
DEBUG = True



class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
	DEBUG = True
	SECRET_KEY ='t0p s3cr3t'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:himanshi@localhost/login'


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:himanshi@localhost/login'

class ProductionConfig(Config):
	DEBUG = False
	SECRET_KEY ='t0p s3cr3t'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://myprojectuser:himanshi@localhost/myproject'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
